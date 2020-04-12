class batch_dealing():
    def __init__(self, sheet_id,body = {}, requests = []):
        self.body = body
        self.sheet_id = sheet_id
        self.requests = requests
        self.range = {}
    
    def get_body(self):
        return self.body

    def update_body(self):
        self.body = {
            'requests' : self.requests
        }

    def set_range(self,srow,erow,scol,ecol):

        self.range = {
            "sheetId" : self.sheet_id,
            "startRowIndex": srow -1,
            "endRowIndex": erow,
            "startColumnIndex": scol -1,
            "endColumnIndex": ecol
        }

    def merge_cells(self,start_row, end_row, start_col, end_col, all_mode = True):

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
                        "range" : self.range,
                        "mergeType": "MERGE_COLUMNS"
                    }
                }
            )
        self.update_body()

    def set_color(self,rgb,row, column):
        self.requests.append({
                "repeatCell":{
                    "range": {
                        "sheetId": self.sheet_id,
                        "startRowIndex": row-1,
                        "endRowIndex": row,
                        "startColumnIndex": column-1,
                        "endColumnIndex": column
                    },
                    "cell" : {
                        "userEnteredFormat" : {
                            "backgroundColor" : {
                                    "red" : rgb[0],
                                    "green" : rgb[1],
                                    "blue" : rgb[2]
                            }
                        }
                    },
                    "fields" : "userEnteredFormat.backgroundColor"
                }
            }
        )
        self.update_body()
        
    def set_color_range(self,rgb,srow,erow, scolumn, ecolumn):
        self.requests.append({
                "repeatCell":{
                    "range": {
                        "sheetId": self.sheet_id,
                        "startRowIndex": srow-1,
                        "endRowIndex": erow,
                        "startColumnIndex": scolumn-1,
                        "endColumnIndex": ecolumn
                    },
                    "cell" : {
                        "userEnteredFormat" : {
                            "backgroundColor" : {
                                    "red" : rgb[0],
                                    "green" : rgb[1],
                                    "blue" : rgb[2]
                            }
                        }
                    },
                    "fields" : "userEnteredFormat.backgroundColor"
                }
            }
        )
        self.update_body()
    
    def alignment(self,align, row, column):
        self.requests.append({
            "repeatCell": {
                    "range": {
                        "sheetId": self.sheet_id,
                        "startRowIndex": row-1,
                        "endRowIndex": row,
                        "startColumnIndex": column-1,
                        "endColumnIndex": column
                    },
                    "cell" : {
                        "userEnteredFormat":{
                                "horizontalAlignment" : align,
                                "verticalAlignment" : align
                        }
                    },
                    "fields" : "userEnteredFormat(horizontalAlignment,verticalAlignment)"
                }
            }
         )
        self.update_body()

    def alignment_range(self,align, srow, erow, scolumn, ecolumn, vertical = 'MIDDLE'):
        self.requests.append({
            "repeatCell": {
                    "range": {
                        "sheetId": self.sheet_id,
                        "startRowIndex": srow-1,
                        "endRowIndex": erow,
                        "startColumnIndex": scolumn-1,
                        "endColumnIndex": ecolumn
                    },
                    "cell" : {
                        "userEnteredFormat":{
                                "horizontalAlignment" : align,
                                "verticalAlignment" : vertical,
                        }
                    },
                    "fields" : "userEnteredFormat(horizontalAlignment,verticalAlignment)"
                }
            }
         )
        self.update_body()

    def font_size(self,size, row, column, bold = False, font = 'Roboto'):
        self.requests.append({
                "repeatCell": {
                    "range" : {
                        "sheetId" : self.sheet_id,
                        "startRowIndex" : row-1,
                        "endRowIndex" : row,
                        "startColumnIndex": column-1,
                        "endColumnIndex" : column
                    },
                    "cell" : {
                        "userEnteredFormat": {
                            "textFormat" : {
                                "fontSize" : size,
                                "fontFamily" : font,
                                "bold" : bold
                            }
                        }
                    },
                    "fields" : "userEnteredFormat.textFormat"
                }
            }
        )
        self.update_body()

    #Styles : DOTTED, DASHED, SOLID, SOLID_MEDIUM, SOLID_THICK, DOUBLE
    def set_borders(self, color, style, row, col):     
        self.requests.append({
            "updateBorders" : {
                "range" : {
                    "sheetId": self.sheet_id,
                    "startRowIndex": row-1,
                    "endRowIndex": row,
                    "startColumnIndex": col-1,
                    "endColumnIndex": col
                },
                "top": {
                    "style" : style,
                    "width" : 1,
                    "color" : {
                        "red": color[0],
                        "green": color[1],
                        "blue" : color[2]
                    }
                },
                "bottom": {
                    "style" : style,
                    "width" : 1,
                    "color" : {
                        "red": color[0],
                        "green": color[1],
                        "blue" : color[2]
                    }
                },
                "left": {
                    "style" : style,
                    "width" : 1,
                    "color" : {
                        "red": color[0],
                        "green": color[1],
                        "blue" : color[2]
                    }
                },
                "right": {
                    "style" : style,
                    "width" : 1,
                    "color" : {
                        "red": color[0],
                        "green": color[1],
                        "blue" : color[2]
                    }
                },
            }
        })
        self.update_body()

    def set_borders_range(self, color, style, start_row,end_row, start_col, end_col):     
        self.requests.append({
            "updateBorders" : {
                "range" : {
                    "sheetId": self.sheet_id,
                    "startRowIndex": start_row-1,
                    "endRowIndex": end_row,
                    "startColumnIndex": start_col-1,
                    "endColumnIndex": end_col
                },
                "top": {
                    "style" : style,
                    "width" : 1,
                    "color" : {
                        "red": color[0],
                        "green": color[1],
                        "blue" : color[2]
                    }
                },
                "bottom": {
                    "style" : style,
                    "width" : 1,
                    "color" : {
                        "red": color[0],
                        "green": color[1],
                        "blue" : color[2]
                    }
                },
                "left": {
                    "style" : style,
                    "width" : 1,
                    "color" : {
                        "red": color[0],
                        "green": color[1],
                        "blue" : color[2]
                    }
                },
                "right": {
                    "style" : style,
                    "width" : 1,
                    "color" : {
                        "red": color[0],
                        "green": color[1],
                        "blue" : color[2]
                    }
                },
            }
        })
        self.update_body()

    def change_sheet_name(self,name):
        self.requests.append({
               "updateSheetProperties": {
                    "properties" : {"title" : name},
                    "fields" : "title" 
                }
            }
        )
        self.update_body()      

    def set_number_format(self,row,col):
        self.requests.append({
            "repeatCell":{
                "range": {
                    "sheetId" : self.sheet_id,
                    "startRowIndex": row-1,
                    "endRowIndex": row,
                    "startColumnIndex": col-1,
                    "endColumnIndex" : col,
                },
                "cell": {
                    "userEnteredFormat": {
                        "numberFormat": {
                            "type": "NUMBER",
                            "pattern": "#.##"
                        }
                    }
                },
                "fields" : "userEnteredFormat.numberFormat"
            }
        })
        self.update_body()

    def set_date_format(self,row,col):
        self.requests.append({
            "repeatCell":{
                "range": {
                    "sheetId" : self.sheet_id,
                    "startRowIndex": row-1,
                    "endRowIndex": row,
                    "startColumnIndex": col-1,
                    "endColumnIndex" : col,
                },
                "cell": {
                    "userEnteredFormat": {
                        "numberFormat": {
                            "type": "DATE",
                            "pattern": "dd/mm/yyyy"
                        }
                    }
                },
                "fields" : "userEnteredFormat.numberFormat"
            }
        })
        self.update_body()
