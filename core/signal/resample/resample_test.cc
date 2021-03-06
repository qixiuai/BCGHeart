#include <iostream>
#include <vector>

#include "resample.h"

using namespace std;

int main ()
{
  vector<int> input;
  vector<float> output;
  float x1[]={1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0};
  for (int i = 0; i < 10; i++) {
    x1[i] *= 10;
  }
  input.assign( x1, x1 + 10 );
  //resample ( 2, 3, input, output );
  output = resample(input, 2, 3);
  for ( int i = 0, n = output.size(); i < n; i++ )
    cout << output[i] << " ";
  cout<<endl;
  cout << input.size() << ',' << output.size() << endl;
  return 0;
}
