import os
from PIL import Image
from tqdm import tqdm  # 进度条


def CreateGIF(imgFolderPath, width, height, Resize_flag=0, loop_num=0, duration_num=1000, sort = False):
    '''
    This fuction is used to create a GIF file from a Folder
    To make the best expression, it is recommended to sort the files so that the GIF will display correctly
    :param imgFolderPath: String type, Where the static pics are
    :param width: Int type, Target Picture Width
    :param height: Int type, Target Picture Height
    :param Resize_flag: Int type, 1 for true 0 for false, it can be set on when the pics are not in same size
    :param loop_num:  Int type, loop times in GIF file
    :param duration_num:  Int type, how long (ms) you want it takes between two pics in a GIF
    :param sort: Bool type, True to sort the Pics in the Folder(100, 110, 11  to  11, 100, 110)
    :return:
    '''
    fileList = os.listdir(imgFolderPath)
    if sort:
        fileList.sort(key=lambda x: int(x[:-4]))    # -4 is to filter the ".png" or ".jpg"
    firstImgPath = os.path.join(imgFolderPath, fileList[0])
    if (0 == Resize_flag):
        im = Image.open(firstImgPath)
    else:
        im = Image.open(firstImgPath).resize((width, height), Image.ANTIALIAS)  # 保证所有的图片最终出来是相同的size

    images = []
    # for img in fileList[1:]:                   #不显示读条
    for img in tqdm(fileList[1:], '生成GIF中'):  # 显示读条
        print(img)
        imgPath = os.path.join(imgFolderPath, img)
        if (0 == Resize_flag):
            images.append(Image.open(imgPath))
        else:
            images.append(Image.open(imgPath).resize((width, height), Image.ANTIALIAS))  # 保证所有的图片最终出来是相同的size

    im.save('Result.gif', save_all=True, append_images=images, loop=loop_num,
            duration=duration_num)