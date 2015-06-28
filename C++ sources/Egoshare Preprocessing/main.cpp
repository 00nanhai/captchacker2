#include <cv.hpp>
#include <cxcore.hpp>
#include <highgui.h>
#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <sstream>

#if defined (WIN32)
#pragma comment(lib,"cv")
#pragma comment(lib,"cvaux")
#pragma comment(lib,"cxcore")
#pragma comment(lib,"highgui")
#pragma comment(lib,"cvcam")
#endif

using namespace std;


#define WIDTH 20
#define HEIGHT 20



template <class T>
inline std::string to_string (const T& t)
{
	std::stringstream ss;
	ss << t;
	return ss.str();
}




typedef struct CC
{
	CvConnectedComp *comp;
	IplImage *mask;
};




inline int func_compare_area_cc(const void *a, const void *b)
{
	//Ordre décroissant par aire
	return (*((CC**) b))->comp->area - (*((CC**) a))->comp->area;
}

inline int func_compare_pos_cc(const void *a, const void *b)
{
	//cout << "COMPARISON: " << (*((CC**) a))->comp->rect.x << " " << (*((CC**) b))->comp->rect.x << endl;
	//Ordre croissant par position
	return (*((CC**) a))->comp->rect.x - (*((CC**) b))->comp->rect.x;
}










int main(int argc, char *argv[])
{
	//Noms de fichiers
	string filenameIN;
	if (argc < 2)
		filenameIN = "test.jpg";
	else
		filenameIN = argv[1];


	//Seuillage
	int threshold = 150, maxValue = 255;
	int thresholdType = CV_THRESH_BINARY;

	IplImage *srcImg=0, *grayThresh=0, *gray4=0, *gray8=0;
	srcImg = cvLoadImage(filenameIN.c_str(),1);

	grayThresh = cvCreateImage( cvSize(srcImg->width, srcImg->height), IPL_DEPTH_8U, 1 );
	cvCvtColor(srcImg, grayThresh, CV_BGR2GRAY );
	cvThreshold(grayThresh, grayThresh, threshold, maxValue, thresholdType);

	int connectivity, size;

	//On commence par chercher les composantes 8-connexes
	connectivity = 4;
	std::vector<CC*> CCs4;


	gray4 = cvCloneImage(grayThresh);

	//Sélection de toutes les composantes connexes en noir
	for (int i=0; i<gray4->width; ++i)
	{
		for (int j=0; j<gray4->height; ++j)
		{
			if (cvGet2D(gray4, j, i).val[0] == 0)
			{
				CvConnectedComp *comp = new CvConnectedComp;

				IplImage *mask = cvCreateImage(cvSize(gray4->width+2, gray4->height+2), IPL_DEPTH_8U, 1);
				cvZero(mask);

				cvFloodFill(gray4, cvPoint(i,j), cvScalar(128),cvScalarAll(0),cvScalarAll(0),comp, connectivity, mask);

				CC *cc = new CC;
				cc->mask = mask;
				cc->comp = comp;
				CCs4.push_back(cc);
			}
		}
	}

	//cout << CCs4.size() << " connected 4-components found." << endl;

	//Tri décroissant selon l'aire des composantes connexes
	qsort(&CCs4[0], CCs4.size(), sizeof(CCs4[0]), func_compare_area_cc);

	//On ne garde que 3 composantes connexes
	size = CCs4.size();
	for (int i=3; i<size; ++i)
		CCs4.pop_back();




	//On commence par chercher les composantes 8-connexes
	connectivity = 8;
	std::vector<CC*> CCs8;

	gray8 = cvCloneImage(grayThresh);

	//Sélection de toutes les composantes connexes en noir
	for (int i=0; i<gray8->width; ++i)
	{
		for (int j=0; j<gray8->height; ++j)
		{
			if (cvGet2D(gray8, j, i).val[0] == 0)
			{
				CvConnectedComp *comp = new CvConnectedComp;

				IplImage *mask = cvCreateImage(cvSize(gray8->width+2, gray8->height+2), IPL_DEPTH_8U, 1);
				cvZero(mask);

				cvFloodFill(gray8, cvPoint(i,j), cvScalar(128),cvScalarAll(0),cvScalarAll(0),comp, connectivity, mask);

				CC *cc = new CC;
				cc->mask = mask;
				cc->comp = comp;
				CCs8.push_back(cc);
			}
		}
	}

	//cout << CCs8.size() << " connected 8-components found." << endl;

	//Tri décroissant selon l'aire des composantes connexes
	qsort(&CCs8[0], CCs8.size(), sizeof(CCs8[0]), func_compare_area_cc);

	//On ne garde que 3 composantes connexes
	size = CCs8.size();
	for (int i=3; i<size; ++i)
		CCs8.pop_back();



	std::vector<CC*> CCs;

	if (CCs8.size() < 3)
	{
		CCs = CCs4;
		//cout << "4" << endl;
	}
	else
	{
		//Si une des composantes 4-connexes est un fragment de caractère,
		//on cherche les composantes 8-connexes
		if (CCs4[2]->comp->area < 30)
		{
			CCs = CCs8;
			//cout << "8" << endl;
		}
		else
		{
			CCs = CCs4;
			//cout << "4" << endl;
		}
	}


	//Tri croissant selon l'abscisse de la composante connexe
	qsort(&CCs[0], CCs.size(), sizeof(CCs[0]), func_compare_pos_cc);



	std::vector<IplImage*> letters;
	for (int i=0; i<3; ++i)
	{
		IplImage *letter = new IplImage;
		letter = cvCreateImage( cvSize(WIDTH, HEIGHT), IPL_DEPTH_8U, 1 );
		cvFillImage(letter, 255);
		letters.push_back(letter);
	}

	//Remplissage des imagettes par les sous-rectangles de l'image thresholdée
	for (int index_image=0; index_image<letters.size(); ++index_image)
	{
		IplImage *letter = letters[index_image];
		CC *cc = CCs[index_image];

		int offsetx = (WIDTH -  cc->comp->rect.width)/2;
		int offsety = (HEIGHT - cc->comp->rect.height)/2;

		//cout << cc->comp->rect.width<< " " << cc->comp->rect.height << endl;
		//Recopiage de la sous-image
		for (int i=1; i<cc->mask->width-1; ++i)
		{
			for (int j=1; j<cc->mask->height-1; ++j)
			{
				if (cvGet2D(cc->mask, j, i).val[0] == 1)
				{
					int Y = j - cc->comp->rect.y + offsety;
					int X = i - cc->comp->rect.x + offsetx;

					if ((X>0) && (X<WIDTH) && (Y>0) && (Y<HEIGHT))
					{
						cvSet2D(letter,
							j - cc->comp->rect.y + offsety,
							i - cc->comp->rect.x + offsetx,
							cvScalar(0));
					}
				}
			}
		}

		//cout << "Lettre " << index_image << " preprocessed!" << endl;
	}



	//Sauvegardes des imagettes
	std::string filename = "letter";;
	for (int i=0; i<3; ++i)
		cvSaveImage((filename+to_string(i+1)+".bmp").c_str(), letters[i]);


	//if(!cvSaveImage("testOUT.bmp".c_str(),grayThresh)){
	//    cout << "WARNING: Pic can't be saved" <<endl;
	//    exit(2);
	//}
	//cout << "testOUT.bmp" << " successfully written" << endl;

	//cvWaitKey(0);
	cvReleaseImage( &grayThresh );
	cvReleaseImage( &srcImg );

	//system("pause");

	return 0;


}
