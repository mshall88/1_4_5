import PIL
import matplotlib.pyplot as plt # single use of plt is commented out
import os.path  
import PIL.ImageDraw
import webcolors           

def frame_edges(original_image, wide, color):
    
    old_size = original_image.size

    new_size = (old_size[0]+wide, old_size[1]+wide)
    new_im = PIL.Image.new("RGB", new_size, color)   
    new_im.paste(original_image, ((new_size[0]-old_size[0])/2,
                            (new_size[1]-old_size[1])/2))

    width, height = new_im.size
    
    frame_mask = PIL.Image.new('RGBA', (width, height), (127,0,127,0))
    drawing_layer = PIL.ImageDraw.Draw(frame_mask)
    
    drawing_layer.polygon([(0,0),(width,0),
                            (width,height),(0,height)],
                            fill=(127,0,127,255))
    
    
    # Make the new image, starting with all transparent
    result = PIL.Image.new('RGBA', new_im.size, (0,0,0,0))
    result.paste(new_im, (0,0), mask=frame_mask)
    return result
    
def get_images(directory=None):
    
    if directory == None:
        directory = os.getcwd() # Use working directory if unspecified
        
    image_list = [] # Initialize aggregaotrs
    file_list = []
    
    directory_list = os.listdir(directory) # Get list of files
    for entry in directory_list:
        absolute_filename = os.path.join(directory, entry)
        try:
            image = PIL.Image.open(absolute_filename)
            file_list += [entry]
            image_list += [image]
        except IOError:
            pass # do nothing with errors tying to open non-images
    return image_list, file_list

def frame_edges_of_all_images(wide, color, directory=None):
    
    if directory == None:
        directory = os.getcwd() # Use working directory if unspecified
        
    # Create a new directory 'Framed'
    new_directory = os.path.join(directory, 'Framed')
    try:
        os.mkdir(new_directory)
    except OSError:
        pass # if the directory already exists, proceed  
    
    #load all the images
    image_list, file_list = get_images(directory)  
    color = webcolors.name_to_rgb(color)
    #go through the images and save modified versions
    for n in range(len(image_list)):
        # Parse the filename
        filename, filetype = file_list[n].split('.')
        
        
        new_image = frame_edges(image_list[n],wide,color)
        #save the altered image, suing PNG to retain transparency
        new_image_filename = os.path.join(new_directory, filename + '.png')
        new_image.save(new_image_filename)  
        
frame = raw_input("Would you like to frame some pictures? (y or n): \n")
if frame == "y":
    color = raw_input("Type the color you would like the frame to be: \n")
    wide = int(raw_input("What pixel size would you like your frame to be: \n"))
    all_folder = raw_input("Would you like to frame all pictures in your folder? (y or n): \n")
    if all_folder == "n":
        print "Okay! Here\'s a framed photo of your favorite PLTW master teacher!"
        frame_edges((PIL.Image.open(os.getcwd()+"/Images/Doyle.jpg")), wide, color).show()
    else:
        print "Sweet! Check your folder!"
        frame_edges_of_all_images(wide, color, "/Users/teacher/Desktop/PLTW/CSE 2014 Training/1.4.4 SourceFiles/Images")
else:
    print "Fine then...."
           