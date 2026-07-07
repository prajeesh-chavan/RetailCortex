import argparse
import logging
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("pipeline")

ALL_ENTITIES = [
    "customer",
    "order",
    "product",
    "sales_channel",
    "carrier",
    "category",
    "promotion",
    "address",
    "brand",
    "vendor",
    "vendor_address",
    "customer_address",
    "product_variant",
    "warehouse",
    "inventory",
    "inventory_movement",
    "order_item",
    "order_address",
    "order_status_history",
    "payment",
    "refund",
    "shipment",
    "shipment_item",
    "returns",
    "return_item",
    "order_item_discount",
    "product_review",
    "cart",
    "cart_item",
    "customer_event",
]

DBT_DIR = Path(__file__).resolve().parent / "dbt_retail"


def _checkpoint_exists(entity):
    return (Path("data") / "checkpoints" / entity).exists()


def _run_subprocess(cmd, cwd=None, timeout=None):
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Process timed out"
    except FileNotFoundError:
        return -2, "", f"Command not found: {cmd[0]}"


def run_bronze(entity, timeout):
    logger.info(f"[bronze] Starting {entity} (timeout={timeout}s)")
    start = time.time()
    rc, stdout, stderr = _run_subprocess(
        ["python", "-m", f"src.bronze.{entity}"],
        timeout=timeout,
    )
    elapsed = time.time() - start
    if rc == -1:
        logger.info(f"[bronze] {entity} timed out after {timeout}s — partial data expected")
        return True, elapsed
    if rc != 0:
        logger.error(f"[bronze] {entity} failed (rc={rc})\n{stderr[:500]}")
        return False, elapsed
    logger.info(f"[bronze] {entity} completed in {elapsed:.1f}s")
    return True, elapsed


def run_silver(entity):
    logger.info(f"[silver] Starting {entity}")
    start = time.time()
    rc, stdout, stderr = _run_subprocess(
        ["python", "-m", f"src.silver.{entity}"],
    )
    elapsed = time.time() - start
    if rc != 0:
        logger.error(f"[silver] {entity} failed (rc={rc})\n{stderr[:500]}")
        return False, elapsed
    logger.info(f"[silver] {entity} completed in {elapsed:.1f}s")
    return True, elapsed


def run_dbt():
    results = {}
    for cmd_name, cmd_args in [("dbt run", ["dbt", "run"]), ("dbt test", ["dbt", "test"])]:
        logger.info(f"[dbt] Starting {cmd_name}")
        start = time.time()
        rc, stdout, stderr = _run_subprocess(cmd_args, cwd=DBT_DIR)
        elapsed = time.time() - start
        results[cmd_name] = {"rc": rc, "stdout": stdout, "elapsed": elapsed}
        logger.info(f"[dbt] {cmd_name} completed in {elapsed:.1f}s (rc={rc})")
        if rc != 0:
            break
    return results


def run_phase(entities, phase_fn, phase_name, **kwargs):
    results = {}
    with ThreadPoolExecutor(max_workers=kwargs.get("parallel", 1)) as executor:
        futures = {
            executor.submit(phase_fn, entity, **{k: v for k, v in kwargs.items() if k != "parallel"}): entity
            for entity in entities
        }
        for future in as_completed(futures):
            entity = futures[future]
            success, elapsed = future.result()
            results[entity] = {"success": success, "elapsed": elapsed}
    return results


def print_separator(char="=", width=72):
    logger.info(char * width)


def print_phase_summary(results, phase_name):
    passed = sum(1 for r in results.values() if r["success"])
    failed = len(results) - passed
    total_elapsed = sum(r["elapsed"] for r in results.values())
    for entity, r in results.items():
        status = "[PASS]" if r["success"] else "[FAIL]"
        logger.info(f"  {status} {entity:<25s} ({r['elapsed']:.1f}s)")
    logger.info(f"  {'─' * 40}")
    logger.info(f"  {passed}/{len(results)} passed  |  {failed} failed  |  total {total_elapsed:.1f}s")
    return failed


def parse_args():
    parser = argparse.ArgumentParser(
        description="RetailCortex medallion pipeline orchestrator"
    )
    parser.add_argument(
        "--entities",
        help="Comma-separated entity list (default: all 30 entities)",
    )
    parser.add_argument(
        "--bronze-timeout",
        type=int,
        default=60,
        help="Seconds per bronze entity before kill (default: 60)",
    )
    parser.add_argument(
        "--skip-bronze",
        action="store_true",
        help="Skip bronze phase",
    )
    parser.add_argument(
        "--skip-silver",
        action="store_true",
        help="Skip silver phase",
    )
    parser.add_argument(
        "--skip-dbt",
        action="store_true",
        help="Skip dbt phase",
    )
    parser.add_argument(
        "--parallel",
        type=int,
        default=1,
        help="Parallel entity count (default: 1, sequential)",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Skip entities with existing checkpoints",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    start_time = time.time()

    entities = args.entities.split(",") if args.entities else ALL_ENTITIES

    if args.resume:
        skipped = [e for e in entities if _checkpoint_exists(e)]
        entities = [e for e in entities if e not in skipped]
        if skipped:
            logger.info(f"Resume mode: skipping {len(skipped)} entities with existing checkpoints")

    print_separator()
    logger.info(f"Pipeline Run | {len(entities)} entities | parallel={args.parallel}")
    logger.info(f"Bronze timeout: {args.bronze_timeout}s/entity")
    if args.skip_bronze:
        logger.info("Bronze phase: SKIPPED")
    if args.skip_silver:
        logger.info("Silver phase: SKIPPED")
    if args.skip_dbt:
        logger.info("dbt phase: SKIPPED")
    print_separator()

    pipeline_failed = False

    if not args.skip_bronze and entities:
        print_separator("-")
        logger.info("PHASE 1: BRONZE INGESTION")
        print_separator("-")
        bronze_results = run_phase(
            entities,
            run_bronze,
            "bronze",
            timeout=args.bronze_timeout,
            parallel=args.parallel,
        )
        bronze_failed = print_phase_summary(bronze_results, "bronze")
        if bronze_failed:
            failed_entities = [e for e, r in bronze_results.items() if not r["success"]]
            logger.warning(f"Skipping silver for {bronze_failed} failed bronze entities")
            entities = [e for e in entities if e not in failed_entities]

    if not args.skip_silver and entities:
        print_separator("-")
        logger.info("PHASE 2: SILVER TRANSFORMATION")
        print_separator("-")
        silver_results = run_phase(
            entities,
            run_silver,
            "silver",
            parallel=args.parallel,
        )
        silver_failed = print_phase_summary(silver_results, "silver")
        if silver_failed:
            pipeline_failed = True

    if not args.skip_dbt:
        print_separator("-")
        logger.info("PHASE 3: DBT")
        print_separator("-")
        dbt_results = run_dbt()
        for cmd, r in dbt_results.items():
            status = "[PASS]" if r["rc"] == 0 else "[FAIL]"
            logger.info(f"  {status} {cmd:<25s} ({r['elapsed']:.1f}s)")
        if any(r["rc"] != 0 for r in dbt_results.values()):
            pipeline_failed = True

    total_elapsed = time.time() - start_time
    print_separator()
    if pipeline_failed:
        logger.error(f"Pipeline finished with ERRORS | Duration: {total_elapsed:.1f}s")
        sys.exit(1)
    else:
        logger.info(f"Pipeline completed successfully | Duration: {total_elapsed:.1f}s")


if __name__ == "__main__":
    main()
