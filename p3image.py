# P3image.py
# Nick Fogg (nsfogg)
# 10/20/2023

import sys

RGB_PIXEL_NUM = 3

# Class for defining image object
class P3image:

    # Image has ascii type, comment, area dimensions, and color code
    # as well as a list of rgb values stored in a list
    def __init__(self, ascii, comment, area, color_code):
        self.__ascii = ascii
        self.__comment = comment
        self.__area = area
        self.__color_code = color_code
        self.__rgb = []
    
    # Open file, read image data, store in obj
    def load_image(self, name):
        try:
            with open(name, "r") as infile:
                count = 0
                idx = 0
                row = []
                for line in infile:
                    # Check if top 4 lines (header)
                    if count > RGB_PIXEL_NUM:
                        if idx < self.__area[0] * RGB_PIXEL_NUM:
                            row.append(int(line.strip()))
                        else:
                            # Grow the list as rows and columns
                            self.__rgb.append(row)
                            row = []
                            row.append(int(line.strip()))
                            idx = 0
                        idx = idx + 1
                    count = count + 1
                self.__rgb.append(row)
        except:
            sys.exit("Execution terminated.")

    # open file, write image data to file, close file
    def output_image(self, name):
        try:
            # Print file information starting with header
            with open(name, "w") as outfile:
                outfile.write(f"{self.__ascii}\n")
                outfile.write(f"{self.__comment}\n")
                outfile.write(f"{self.__area[0]} {self.__area[1]}\n")
                outfile.write(f"{self.__color_code}\n")
                # Print each rgb value in list
                for i in range(len(self.__rgb)):
                    for j in range(RGB_PIXEL_NUM * self.__area[0]):                        
                        outfile.write(f"{self.__rgb[i][j]}\n")
        except:
            sys.exit("Execution terminated.")
    
    # Return rgb value at a certain point in the list
    def get_rgb_value(self, row, col):
        return self.__rgb[row][col]
    
    # Sets the rgb list for an image
    def set_rgb(self, list):
        for i in range(len(list)):
            self.__rgb.append(list[i])
    
    # override class method to output image comment, ascii, width
    # and height
    def __str__(self):
        return f"{self.__comment}\nType: {self.__ascii}\nWidth: {self.__area[0]} Height: {self.__area[1]}"