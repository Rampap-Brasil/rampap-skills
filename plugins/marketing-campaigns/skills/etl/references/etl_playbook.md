# ETL Playbook

> Folder paths and sheet/column names below are literal identifiers from the source system
> and are kept verbatim.

1. Bring the Excel file from the folder `gestores/planejamento e estrategia/comercial/Campanhas PRs MM/YY`;
2. Make a copy of the Excel file into `gestores/planejamento e estrategia/comercial/Campanhas PRs MM/YY`; it will be the template for the campaign planning;
3. Generate the Excel file from the Sankhya MRP screen and bring it into the project, dated with the last closed day;
4. Clear the data of the `MRP ativos` sheet, keeping only the headers;
5. Remove the first two rows and the last row of the Excel file sent by the user;
6. Copy the data from columns A4 through column CK and paste it into the `MRP ativos` sheet of the template Excel file;
7. Delete the rows where the `Ativo` column is not "N";
8. Clear the cells from "A2" to the end of column "CK" of the `IT PR1` sheet, keeping only the headers;
9. Paste the data copied from the `MRP ativos` sheet into the `IT PR1` sheet of the template Excel file;
10. Delete the rows where the `Ruptura` column is not "S".
