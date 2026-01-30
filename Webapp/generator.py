import csv

STYLE_BLOCK = """<!-- Responsive Gig Grid Block -->
<style>
  .gig-square {
    width: 100% !important;
    height: 0 !important;
    padding-bottom: 100% !important;
    background-size: cover !important;
    background-position: center center !important;
    background-repeat: no-repeat !important;
    display: block !important;
  }

  @media only screen and (max-width: 620px) {
    .gig-column {
      display: block !important;
      width: 100% !important;
      max-width: 100% !important;
    }
    .gig-cell {
      padding: 10px 0 !important;
    }
    .gig-inner {
      padding: 0 10px !important;
      box-sizing: border-box !important;
    }
  }
</style>
"""

TABLE_OPEN = """<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width:600px; margin:0 auto;">"""
TABLE_CLOSE = "</table>"

CELL_TEMPLATE = """<td class="gig-column gig-cell" width="33.33%" valign="top" style="padding:10px;" align="center">
  <div class="gig-inner">
    <a href="{event_link}" style="text-decoration:none;">
      <div class="gig-square" style="background-image:url('{image_url}');"></div>
    </a>
    <p style="font-family:Arial, sans-serif; font-size:14px; line-height:1.4; margin:5px 0 0; text-align:center;">
      <strong><a href="{event_link}" style="color:#000; text-decoration:none;">{event_name}</a></strong><br>
      {date} <br> {time} &middot; {price}
    </p>
  </div>
</td>"""

def generate_event_cells(csv_path: str) -> list[str]:
    cells = []

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

    if len(rows) < 3:
        raise ValueError("The CSV must contain at least 3 events.")

    if len(rows) % 3 != 0:
        raise ValueError("The number of events must be a multiple of 3.")

    for index, row in enumerate(rows, start=1):
        if len(row) != 6:
            raise ValueError(f"Row {index} does not have exactly 6 columns.")

        event_name, date, time, price, event_link, image_url = row

        cell_html = CELL_TEMPLATE.format(
            event_name=(
                event_name
                .replace(" +", "<br>+", 1)
                .replace(": ", ":<br>", 1)
            ),
            date=date.strip(),
            time=time.strip(),
            price=price.replace("£", "&pound;"),
            event_link=event_link.strip(),
            image_url=image_url.strip()
        )

        cells.append(cell_html)

    return cells

def group_into_rows(cells: list[str], per_row: int = 3) -> list[str]:
    rows = []

    for i in range(0, len(cells), per_row):
        row_cells = cells[i:i + per_row]

        while len(row_cells) < per_row:
            row_cells.append('<td width="33.33%" style="padding:10px;"></td>')

        row_html = "<tr>\n" + "\n".join(row_cells) + "\n</tr>"
        rows.append(row_html)

    return rows

def generate_html_from_csv(csv_path: str) -> str:
    cells = generate_event_cells(csv_path)
    rows = group_into_rows(cells)
    return (
        STYLE_BLOCK
        + "\n"
        + TABLE_OPEN
        + "\n"
        + "\n".join(rows)
        + "\n"
        + TABLE_CLOSE
    )
