import google_ss_color
import gs
DIMENTIONS = {'rows': 8, 'columns': 4}
PALETTE = ['LIGHT YELLOW 3', 'LIGHT RED 3',
           'LIGHT ORANGE 3', 'LIGHT PURPLE 2', 'LIGHT RED BERRY 3']


class Table():
    def __init__(self, worksheet, row, col, title):
        self.row_range = (row, row + DIMENTIONS['rows'])
        self.column_range = (col, col + DIMENTIONS['columns'])
        self.title = title
        self.ws = worksheet
        self.format = BatchFormatter(self.ws._properties['sheetId'])
        self.build()

    def build(self):
        start_r, final_r = self.row_range
        start_c, final_c = self.column_range
        # merge cells for title
        self.format.merge_cells(start_r, start_r, start_c, final_c)

        # assign color to the columns
        for row in range(start_r + 1, final_r):
            index = 0
            for index, column in enumerate(range(start_c, final_c + 1)):
                if column == start_c:
                    self.format.set_date_format(row, column)

                if column == start_c + 1 or column == start_c + 2:
                    self.format.set_number_format(row, column)

                self.format.set_color(google_ss_color.rgb(
                    PALETTE[index]), row, column)
                self.format.font_size(10, row, column, bold=True)
                self.format.set_borders((0, 0, 0), "SOLID", row, column)
                index += 1

        # Prom column weight
        self.format.merge_cells(start_r+1, final_r - 1, final_c - 1, final_c-1)
        col = gs.column_type[start_c + 1]

        self.format.font_size(10, start_r, start_c, bold=True)
        self.format.set_borders_range(
            (0, 0, 0), "SOLID", start_r, start_r, start_c, final_c)
        self.format.set_color(google_ss_color.rgb(
            'LIGHT CORNFLOWER 2'), start_r, start_c)
        # setting the alignment
        self.format.alignment_range(
            "CENTER", start_r, final_r, start_c, final_c)

        # once all the process is done succesfully, update the spreadsheet.
        # update request
        self.format.update_body()
        # write title
        self.ws.update_cell(start_r, start_c, self.title)
        self.ws.update_cell(
            start_r + 1, final_c -
            1, f'=PROMEDIO({col}{start_r+1}:{col}{final_r - 1})'
        )  # add the formule


class BatchFormatter():
    def __init__(self, sheet_id, body={}, requests=[]):
        self.body = body
        self.sheet_id = sheet_id
        self.requests = requests
        self.range = {}

    def get_body(self):
        return self.body

    def update_body(self):
        self.body = {
            'requests': self.requests
        }

    def set_range(self, srow, erow, scol, ecol):

        self.range = {
            "sheetId": self.sheet_id,
            "startRowIndex": srow - 1,
            "endRowIndex": erow,
            "startColumnIndex": scol - 1,
            "endColumnIndex": ecol
        }

    def merge_cells(self, start_row, end_row, start_col, end_col, all_mode=True):

        self.set_range(start_row, end_row, start_col, end_col)
        if all_mode:
            self.requests.append(
                {
                    "mergeCells": {
                        "range": self.range,
                        "mergeType": "MERGE_ALL"
                    }
                }
            )
        else:
            self.requests.append({
                "mergeCells": {
                    "range": self.range,
                    "mergeType": "MERGE_COLUMNS"
                }
            }
            )

    def set_color(self, rgb, row, column):
        self.requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": self.sheet_id,
                    "startRowIndex": row-1,
                    "endRowIndex": row,
                    "startColumnIndex": column-1,
                    "endColumnIndex": column
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": {
                            "red": rgb[0],
                            "green": rgb[1],
                            "blue": rgb[2]
                        }
                    }
                },
                "fields": "userEnteredFormat.backgroundColor"
            }
        }
        )

    def set_color_range(self, rgb, srow, erow, scolumn, ecolumn):
        self.requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": self.sheet_id,
                    "startRowIndex": srow-1,
                    "endRowIndex": erow,
                    "startColumnIndex": scolumn-1,
                    "endColumnIndex": ecolumn
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": {
                            "red": rgb[0],
                            "green": rgb[1],
                            "blue": rgb[2]
                        }
                    }
                },
                "fields": "userEnteredFormat.backgroundColor"
            }
        }
        )

    def alignment(self, align, row, column):
        self.requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": self.sheet_id,
                    "startRowIndex": row-1,
                    "endRowIndex": row,
                    "startColumnIndex": column-1,
                    "endColumnIndex": column
                },
                "cell": {
                    "userEnteredFormat": {
                        "horizontalAlignment": align,
                        "verticalAlignment": align
                    }
                },
                "fields": "userEnteredFormat(horizontalAlignment,verticalAlignment)"
            }
        }
        )

    def alignment_range(self, align, srow, erow, scolumn, ecolumn, vertical='MIDDLE'):
        self.requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": self.sheet_id,
                    "startRowIndex": srow-1,
                    "endRowIndex": erow,
                    "startColumnIndex": scolumn-1,
                    "endColumnIndex": ecolumn
                },
                "cell": {
                    "userEnteredFormat": {
                        "horizontalAlignment": align,
                        "verticalAlignment": vertical,
                    }
                },
                "fields": "userEnteredFormat(horizontalAlignment,verticalAlignment)"
            }
        }
        )

    def font_size(self, size, row, column, bold=False, font='Roboto'):
        self.requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": self.sheet_id,
                    "startRowIndex": row-1,
                    "endRowIndex": row,
                    "startColumnIndex": column-1,
                    "endColumnIndex": column
                },
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {
                            "fontSize": size,
                            "fontFamily": font,
                            "bold": bold
                        }
                    }
                },
                "fields": "userEnteredFormat.textFormat"
            }
        }
        )

    # Styles : DOTTED, DASHED, SOLID, SOLID_MEDIUM, SOLID_THICK, DOUBLE
    def set_borders(self, color, style, row, col):
        self.requests.append({
            "updateBorders": {
                "range": {
                    "sheetId": self.sheet_id,
                    "startRowIndex": row-1,
                    "endRowIndex": row,
                    "startColumnIndex": col-1,
                    "endColumnIndex": col
                },
                "top": {
                    "style": style,
                    "width": 1,
                    "color": {
                        "red": color[0],
                        "green": color[1],
                        "blue": color[2]
                    }
                },
                "bottom": {
                    "style": style,
                    "width": 1,
                    "color": {
                        "red": color[0],
                        "green": color[1],
                        "blue": color[2]
                    }
                },
                "left": {
                    "style": style,
                    "width": 1,
                    "color": {
                        "red": color[0],
                        "green": color[1],
                        "blue": color[2]
                    }
                },
                "right": {
                    "style": style,
                    "width": 1,
                    "color": {
                        "red": color[0],
                        "green": color[1],
                        "blue": color[2]
                    }
                },
            }
        })

    def set_borders_range(self, color, style, start_row, end_row, start_col, end_col):
        self.requests.append({
            "updateBorders": {
                "range": {
                    "sheetId": self.sheet_id,
                    "startRowIndex": start_row-1,
                    "endRowIndex": end_row,
                    "startColumnIndex": start_col-1,
                    "endColumnIndex": end_col
                },
                "top": {
                    "style": style,
                    "width": 1,
                    "color": {
                        "red": color[0],
                        "green": color[1],
                        "blue": color[2]
                    }
                },
                "bottom": {
                    "style": style,
                    "width": 1,
                    "color": {
                        "red": color[0],
                        "green": color[1],
                        "blue": color[2]
                    }
                },
                "left": {
                    "style": style,
                    "width": 1,
                    "color": {
                        "red": color[0],
                        "green": color[1],
                        "blue": color[2]
                    }
                },
                "right": {
                    "style": style,
                    "width": 1,
                    "color": {
                        "red": color[0],
                        "green": color[1],
                        "blue": color[2]
                    }
                },
            }
        })

    def change_sheet_name(self, name):
        self.requests.append({
            "updateSheetProperties": {
                "properties": {"title": name},
                "fields": "title"
            }
        }
        )

    def set_number_format(self, row, col):
        self.requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": self.sheet_id,
                    "startRowIndex": row-1,
                    "endRowIndex": row,
                    "startColumnIndex": col-1,
                    "endColumnIndex": col,
                },
                "cell": {
                    "userEnteredFormat": {
                        "numberFormat": {
                            "type": "NUMBER",
                            "pattern": "#.##"
                        }
                    }
                },
                "fields": "userEnteredFormat.numberFormat"
            }
        })

    def set_date_format(self, row, col):
        self.requests.append({
            "repeatCell": {
                "range": {
                    "sheetId": self.sheet_id,
                    "startRowIndex": row-1,
                    "endRowIndex": row,
                    "startColumnIndex": col-1,
                    "endColumnIndex": col,
                },
                "cell": {
                    "userEnteredFormat": {
                        "numberFormat": {
                            "type": "DATE",
                            "pattern": "dd/mm/yyyy"
                        }
                    }
                },
                "fields": "userEnteredFormat.numberFormat"
            }
        })
