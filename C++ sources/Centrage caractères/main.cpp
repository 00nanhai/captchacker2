#include <iostream>
#include <string>
#include "boost/filesystem.hpp"

#include "cv.h"
#include "cxcore.h"
#include "highgui.h"

#if defined (WIN32)
#pragma comment(lib,"cv")
#pragma comment(lib,"cvaux")
#pragma comment(lib,"cxcore")
#pragma comment(lib,"highgui")
#pragma comment(lib,"cvcam")
#endif

using namespace std;
using namespace boost::filesystem;


void process_file(string filenameIN, int WIDTH, int HEIGHT)
{
	cout << "processing file: " << filenameIN << endl;
	IplImage *srcImg=0, *res=0;

	srcImg = cvLoadImage(filenameIN.c_str(),0);

    if (srcImg) {
        res = cvCreateImage( cvSize(WIDTH, HEIGHT), IPL_DEPTH_8U, 1 );
        cvFillImage(res, 255);

        int xmin=WIDTH, xmax=0, ymin=HEIGHT, ymax=0;
        for (int i=0; i<srcImg->width; ++i)
        {
            for (int j=0; j<srcImg->height; ++j)
            {
                if (cvGet2D(srcImg, j, i).val[0] == 0)
                {
                    if (i<xmin)
                        xmin = i;
                    if (i>xmax)
                        xmax = i;
                    if (j<ymin)
                        ymin=j;
                    if (j>ymax)
                        ymax=j;
                }
            }
        }

        int offsetx = (WIDTH - (xmax-xmin))/2;
        int offsety = (HEIGHT - (ymax-ymin))/2;
        for (int i=0; i<=xmax-xmin; ++i)
        {
            for (int j=0; j<=ymax-ymin; ++j)
            {
                if ((offsety+j>0) && (offsety+j<res->height) && (offsetx+i>0) && (offsetx+i<res->width))
                    cvSet2D(res, offsety+j, offsetx+i, cvGet2D(srcImg, ymin+j, xmin+i));
            }
        }

        cvSaveImage(filenameIN.c_str(), res);
    }
    else {
        cout << "WARNING: File not found!!" << endl;
    }

}


void process_folder(path folder, int WIDTH, int HEIGHT) {
    cout << "Processing "<<folder.string() << " folder... ";
    if ( !exists(folder ) ) {
        cout << "Folder not found. Aborting.";
        exit(1);
    }

    directory_iterator itr(folder), end_itr;

    for ( ; itr != end_itr; ++itr ){
        if (is_directory(itr->status())){
            process_folder(itr->path(), WIDTH, HEIGHT);
        }
        else if (is_regular(itr->status())) {
            string filename = itr->path().filename().string();
            if (filename.substr(filename.length()-3,3) == "bmp") {
                //cout<<itr->leaf()<< " => bmp found!!"<< endl;
                process_file(folder.string()+"/"+itr->path().filename().string(), WIDTH, HEIGHT);
            }
        }

    }
    cout << "Done." << endl;
}



int main(int argc, char *argv[])
{
	path folder;

	int WIDTH;
	int HEIGHT;

	if (argc < 2)
	{
		/*folder = "./DBTraining-Simulation_based";
		WIDTH = 20;
		HEIGHT = 20;*/

		cout << "Usage:"<<endl<<"   Linux:     Centrage path/to/folder WIDTH HEIGHT"<<endl<<"   Windows:   Centrage.exe path/to/folder WIDTH HEIGHT"<<endl;
		exit(1);
	}
	else
	{
		folder = argv[1];
		//cout << "folder IN " << folder << endl;

		WIDTH = atoi(argv[2]);
		//cout << "WIDTH " << WIDTH << endl;

		HEIGHT = atoi(argv[3]);
		//cout << "HEIGHT " << HEIGHT << endl;
	}

	process_folder(folder, WIDTH, HEIGHT);

	return 0;
}




