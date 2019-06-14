
#include <algorithm>
#include <string>
#include <vector>

namespace findpeaks {
  
  class Peak {
  public:
    int peak_index;
    float peak_value;
    int front_index;
    float front_value;
    int back_index;
    float back_value;
    float indicator_value;
    float peak_energy;
    float peak_score;

    bool gt(Peak other);
    bool lr(Peak other);
    bool eq(Peak other);
  };

  class Extrema {
  public:
    int index;
    float value;
    std::string category;
  };

  using PeakList = std::vector<float>;
  PeakList findpeaks(std::vector<float> signal, int min_dist=300, float thres=0.7,
		     std::string direction="up", int energy_window=75);


} // end namespace findpeaks








