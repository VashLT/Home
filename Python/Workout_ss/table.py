from batchFormatter import BatchFormatter
import google_ss_color, gs
DIMENTIONS = {'rows': 8, 'columns': 4}
PALETTE = ['LIGHT YELLOW 3','LIGHT RED 3','LIGHT ORANGE 3','LIGHT PURPLE 2','LIGHT RED BERRY 3']

class Table():
    def __init__(self, worksheet,row, col, title):
        self.row_range = (row, row + DIMENTIONS['rows'])
        self.column_range= (col, col + DIMENTIONS['columns'])
        self.title = title
        self.ws = worksheet
        self.format = BatchFormatter(self.ws._properties['sheetId'])
        self.build()

    def build(self):
        start_r, final_r = self.row_range
        start_c, final_c = self.column_range
        #merge cells for title
        self.format.merge_cells(start_r, start_r, start_c, final_c)

        #assign color to the columns
        for row in range(start_r + 1, final_r):
            index = 0
            for index,column in enumerate(range(start_c , final_c + 1)):
                if column == start_c:
                    self.format.set_date_format(row,column)

                if column == start_c + 1 or column == start_c + 2:
                    self.format.set_number_format(row,column)

                self.format.set_color( google_ss_color.rgb( PALETTE[index] ), row, column)
                self.format.font_size(10, row, column, bold = True)
                self.format.set_borders((0,0,0), "SOLID", row, column)
                index += 1
        
        #Prom column weight    
        self.format.merge_cells(start_r+1, final_r - 1, final_c - 1, final_c-1)
        col = gs.column_type[start_c + 1]

        self.format.font_size(10, start_r, start_c, bold = True)
        self.format.set_borders_range((0,0,0), "SOLID", start_r,start_r,start_c,final_c)
        self.format.set_color( google_ss_color.rgb('LIGHT CORNFLOWER 2'), start_r, start_c)
        #setting the alignment
        self.format.alignment_range("CENTER", start_r, final_r, start_c, final_c)

        # once all the process is done succesfully, update the spreadsheet.
        #update request
        self.format.update_body()
        #write title
        self.ws.update_cell(start_r, start_c, self.title)
        self.ws.update_cell(
            start_r + 1, final_c - 1, f'=PROMEDIO({col}{start_r+1}:{col}{final_r - 1})'
            )  #add the formule