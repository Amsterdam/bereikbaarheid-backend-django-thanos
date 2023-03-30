from import_export.resources import ModelResource

from bereikbaarheid.models import VerkeersTellingen


class VerkeersTellingenResource(ModelResource):
    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        col_mapping = {
            "volgnummer": "volg_nummer",
            "latitude": "lat",
            "longitude": "lon",
            "vma_linknr": "link_nr",
            "telpuntnaam": "telpunt_naam",
            "meetmethode": "meet_methode",
        }

        # all lower
        dataset.headers = [x.strip().lower() for x in dataset.headers]
        # mapping of the model.py columnnames
        dataset.headers = [col_mapping.get(item, item) for item in dataset.headers]

    # def skip_row(self, instance, original, row, import_validation_errors=None):
    #     # skip ontbrekend id in import file = legeregels in csv
    #     if not row["volg_nr"]:
    #         return True

    #     return super().skip_row(instance, original, row, import_validation_errors)

    class Meta:
        model = VerkeersTellingen
        skip_unchanged = True
        report_skipped = True
        exclude = ("xid",)
        import_id_fields = ("volg_nummer",)
