import os
import logging 
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

root_app_path = os.path.dirname(os.path.abspath(__file__))
cred_file_path = os.path.join(root_app_path,'creds.json')


def append_values(_values):
  """Logs data to the google sheet
  """
  spreadsheet_id = "1u0sdq3P5voTJkz-cYZZbmBCvRALheV6RMkx9XErY8rM"
  range_name = "A1:B1"
  value_input_option = "RAW"
  creds, _ = google.auth.load_credentials_from_file(cred_file_path)
  try:
    service = build("sheets", "v4", credentials=creds)
    values = _values

    body = {"values": values}
    result = (
        service.spreadsheets()
        .values()
        .append(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption=value_input_option,
            body=body,
        )
        .execute()
    )
    print(f"{(result.get('updates').get('updatedCells'))} cells appended.")
    return result

  except HttpError as error:
    print(f"An error occurred: {error}")
    return error

# https://docs.google.com/spreadsheets/d/1u0sdq3P5voTJkz-cYZZbmBCvRALheV6RMkx9XErY8rM/edit#gid=0

if __name__ == "__main__":
  append_values(
      [["Testing", "Append"], ["Running", "write_to_sheets.py"]],
  )
