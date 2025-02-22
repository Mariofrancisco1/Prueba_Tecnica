from django.core.management.base import BaseCommand
import pandas as pd
from django.utils import timezone
from prueba1_3.models import Company, Charge

class Command(BaseCommand):
    help = "Cargar los datos desde un archivo CSV"

    def handle(self, *args, **kwargs):
        try:
           
            df = pd.read_csv("prueba1_3/documentos/data_prueba_tecnica.csv")

            
            date_cols = ["created_at", "updated_at"]
            for col in date_cols:
                df[col] = pd.to_datetime(df[col], format="%d/%m/%Y", errors="coerce")

            
            df["amount"] = pd.to_numeric(df["amount"], errors="coerce").round(2)

            
            df.fillna({"status": "Desconocido"}, inplace=True)

            
            companies = {
                row["company_id"]: Company(id=row["company_id"], name=row["company_name"])
                for _, row in df.drop_duplicates(subset=["company_id"]).iterrows()
                if pd.notna(row["company_id"])
            }
            Company.objects.bulk_create(companies.values(), ignore_conflicts=True)

           
            charges = []
            now = timezone.now()

            for _, row in df.iterrows():
                company = companies.get(row["company_id"])
                if not company:
                    continue 

                created_at = row["created_at"] if pd.notna(row["created_at"]) else now
                updated_at = row["updated_at"] if pd.notna(row["updated_at"]) else now

                # Asegurar que las fechas sean "aware"
                if timezone.is_naive(created_at):
                    created_at = timezone.make_aware(created_at)
                if timezone.is_naive(updated_at):
                    updated_at = timezone.make_aware(updated_at)

                charges.append(
                    Charge(
                        id=row["id"],
                        company=company,
                        amount=row["amount"],
                        status=row["status"],
                        created_at=created_at,
                        updated_at=updated_at,
                    )
                )

            
            Charge.objects.bulk_create(charges, ignore_conflicts=True)

            self.stdout.write(self.style.SUCCESS("Transformación y carga completada."))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error en la ejecución: {e}"))
