# image_blender.py
# Nick Fogg (nsfogg)
# 10/20/2023

from p3image import P3image
import sys

ASCII_INDEX = 0
DIMENSIONS_INDEX = 1
COLOR_INDEX = 2
COMMENT_INDEX = 3
NAME_INDEX = 4
MAX_PERCENT = 100
RGB_PIXEL_NUM = 3

def main():
    # Get filename 1 and error check it
    filename1 = input("Enter input filename for image 1: ")
    filename1 = test_file(filename1)[NAME_INDEX]
    # Get filename 2 and error check it
    filename2 = input("Enter input filename for image 2: ")
    filename2 = test_file(filename2)[NAME_INDEX]
    # Blend together
    blend = blend_images(filename1, filename2)
    # Print image
    P3image.output_image(blend, "imageBlend.ppm")
    print("Output file for blended image: imageBlend.ppm")
    print(blend)

# returns image object holding blended image
def blend_images(name1, name2):
    # Get file header parts for both files
    file1 = test_file(name1)
    file2 = test_file(name2)

    # Convert and separate dimensions
    try:
        # Convert dimensions string into iterable list
        file1[1] = [int(i) for i in file1[1].split(" ")]
        file2[1] = [int(i) for i in file2[1].split(" ")]
        if len(file1[1]) != COLOR_INDEX or len(file2[1]) != COLOR_INDEX:
            sys.exit("Execution terminated.")
    except:
        sys.exit("Execution terminated.")

    # Create image objects
    img1 = P3image(file1[ASCII_INDEX], file1[COMMENT_INDEX], file1[DIMENSIONS_INDEX], file1[COLOR_INDEX])
    img2 = P3image(file2[ASCII_INDEX], file2[COMMENT_INDEX], file2[DIMENSIONS_INDEX], file2[COLOR_INDEX])

    # Load images and initialize lists
    P3image.load_image(img1, file1[NAME_INDEX])
    P3image.load_image(img2, file2[NAME_INDEX])

    # Prompt user for weight
    invalid = True
    while invalid:
        try:
            weight = float(input("Enter the weight of the first image: "))
            # Ensure valid input
            if weight < 0 or weight > MAX_PERCENT:
                print("Invalid value entered. Please enter a number between 0-100.")
            else:
                invalid = False
        except ValueError as err:
            # Ask for another entry
            print("Invalid value entered. Please enter a number between 0-100.")

    # Get smallest dimensions so no bad pixel writing in mismatched file sizes
    if file1[1][0] < file2[1][0]:
        width = file1[1][0]
    else:
        width = file2[1][0]
    if file1[1][1] < file2[1][1]:
        height = file1[1][1]
    else:
        height = file2[1][1]
    # Create list to hold width and height
    dimensions = [width, height]

    # Crop images to fit shortest width and height constraints
    color1 = fit_image(width, height, img1)
    color2 = fit_image(width, height, img2)

    # Format comment, color_code, and create blended image
    comment = f"# blended image {weight:.1f}%/{(MAX_PERCENT - weight):.1f}%"
    color_code = file1[COLOR_INDEX]
    blend = P3image("P3", comment, dimensions, color_code)

    # Convert to decimal
    weight = weight / MAX_PERCENT

    # Loop through list and get blended values for each rgb pixel
    rgb = []
    row = []
    for i in range(height):
        for j in range(width * RGB_PIXEL_NUM):
            pixel1 = color1[i][j]
            pixel2 = color2[i][j]
            # Combine weighted pixel amounts from both images
            row.append(int(weight * pixel1 + (1 - weight) * pixel2))
        rgb.append(row)
        row = []

    # Assign the list to the new blended image object
    P3image.set_rgb(blend, rgb)

    return blend

def fit_image(width, height, img):
    colors = []
    row = []
    # Loop through height and width ( times 3 for rgb )
    for i in range(height):
        for j in range(width * RGB_PIXEL_NUM):
            # Get that positions pixel value
            pixel = P3image.get_rgb_value(img, i, j)
            # Add it to the row
            row.append(pixel)
        # Add the row to the entire image mapping
        colors.append(row)
        row = []
    return colors

def test_file(name):
    invalid = True
    img = []
    # Loop while missing or misspelled file name
    while invalid:
        try:
            with open(name, "r") as file:
                invalid = False
                count = 0
                comment = ""
                # Set up image properties found in first 4 lines of header
                for i in range(4):
                    line = file.readline().strip()
                    # Comment could appear in any of first 4 lines
                    if '#' in line:
                        comment = line
                    else:
                        img.append(line)
                img.append(comment)
                # Ensure correct image type
                if img[0] != "P3":
                    print("This file is not in PPM P3 format.")
                    sys.exit("Execution terminated.")
        except IOError as err:
            # Ask user to reenter filename
            name = input("Error reading file, please try again: ")
        except:
            sys.exit("Execution terminated.")
    img.append(name)
    return img

if __name__ == "__main__":
    main()