#include <stdlib.h>
#include <math.h>
#include <stdio.h>
#include <cv.h>
#include <highgui.h>

int main(int argc, char** argv){
  imgName = argv[1];
  Mat image;
  image = imread(imgName, 1);

  if (!image.data){
    printf("something wrong with image");
    return -1;
  }

  Mat grayImg;
  //this function conerts the rgb image to grayscale
  cvtColor(image, grayImg, CV_BGR2GRAY);
  imwrite(Images/Gray.jpg, grayImg);

  namedWindow( "Gray", CV_WINDOW_AUTOSIZE);
  imshow("gray", grayImg);

  waitKey(0);
  return(0);
}
