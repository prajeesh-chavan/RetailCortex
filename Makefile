ENTITIES := customers orders products sales_channels carriers categories promotions addresses brands vendors vendor_addresses customer_addresses product_variants inventory inventory_movements order_items order_addresses order_status_history payments refunds shipments shipment_items returns return_items order_item_discounts

bronze:
	python -m src.bronze.$(ENTITY)

silver:
	python -m src.silver.$(ENTITY)

bronze-all:
	@for entity in $(ENTITIES); do \
		echo ">>> Running bronze pipeline for $$entity..."; \
		python -m src.bronze.$$entity; \
	done

silver-all:
	@for entity in $(ENTITIES); do \
		echo ">>> Running silver pipeline for $$entity..."; \
		python -m src.silver.$$entity; \
	done

dbt-deps:
	cd dbt_retail && dbt deps

dbt-run:
	cd dbt_retail && dbt run

dbt-test:
	cd dbt_retail && dbt test

setup:
	pip install -r requirements.txt

lint:
	ruff check src/

clean:
	rm -rf src/**/__pycache__ .pytest_cache
