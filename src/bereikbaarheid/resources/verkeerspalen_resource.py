from import_export.resources import ModelResource

from bereikbaarheid.models import VerkeersPalen


class VerkeersPalenResource(ModelResource):
    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        col_mapping = {
            "linknr": "link_nr",
            "paalnummer": "paal_nr",
        }

        # all lower
        dataset.headers = [x.strip().lower() for x in dataset.headers]
        # mapping of the model.py columnnames
        dataset.headers = [col_mapping.get(item, item) for item in dataset.headers]

        print(dataset[1])

    def before_import_row(self, row, row_number=None, **kwargs):
        if row["paal_nr"] == "None":
            row["paal_nr"] = ""

    class Meta:
        model = VerkeersPalen
        skip_unchanged = True
        report_skipped = False
        exclude = ("p_id",)
        import_id_fields = ("geometry",)
        import_id_fields = ("link_nr", "dagen", "begin_tijd", "eind_tijd", "geometry")
