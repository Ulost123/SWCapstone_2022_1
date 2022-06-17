import argparse
import os
from random import shuffle
import easydict


parser = easydict.Easydict(
    {
        "train_filename" : "/content/drive/MyDrive/SW_capstone/PCN-main/flist/dataset_3/train.flist",
        "test_filename" : "/content/drive/MyDrive/SW_capstone/PCN-main/flist/dataset_3/test.flist",
        "train_gt_filename" : "/content/drive/MyDrive/SW_capstone/PCN-main/flist/dataset_3/train_gt.flist",
        "test_gt_filename" : "/content/drive/MyDrive/SW_capstone/PCN-main/flist/dataset_3/test_gt.flist",
        "is_shuffled" : 0
    }
)

def write(folder):
    # get the list of directories and separate them into 2 types: training and validation
    training_dirs = os.listdir(folder + "/train")
    testing_dirs = os.listdir(folder + "/test")

    # make 2 lists to save file paths
    training_names = []
    testing_names = []

    # append all files into 2 lists
    for training_item in training_dirs:
        train_flow_item = folder + "/train" + "/" + training_item
        training_names.append(train_flow_item)

    for testing_item in testing_dirs:
        test_flow_item = folder + "/test" + "/" + testing_item
        testing_names.append(test_flow_item)

    # shuffle file names if set
    if args.is_shuffled == 1:
        shuffle(training_names)
        shuffle(testing_names)

    if(folder == '/content/drive/MyDrive/SW_capstone/PCN-main/dataset_3/data_3'):
        train_name = args.train_filename
        test_name = args.test_filename
    else:
        train_name = args.train_gt_filename
        test_name = args.test_gt_filename

    fo = open(train_name, "w")
    fo.write("\n".join(training_names))
    fo.close()

    fo = open(test_name, "w")
    fo.write("\n".join(testing_names))
    fo.close()

    # print process
    print("Written file is: ", train_name, ", is_shuffle: ", args.is_shuffled)


if __name__ == "__main__":

    args = parser.parse_args()

    write('/content/drive/MyDrive/SW_capstone/PCN-main/dataset_3/data_3')
    write('/content/drive/MyDrive/SW_capstone/PCN-main/dataset_3/gt_3')