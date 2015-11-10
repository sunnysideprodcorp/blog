#include <iostream>
#include <vector>


template<typename T, typename S>
void append_to_vector(std::vector<T>& v1, const std::vector<S>& v2) {
    std::cout << "concatting vectors" << std::endl;
  for (auto& e : v2) v1.push_back(e);
}

template<typename T, typename S>
void append_to_vector(std::vector<T>& v1, S v2) {
  std::cout << "got an int instead of a vector" << std::endl;
}
 
template<typename S, typename T>
void append_to_vector(S v1, std::vector<T>& v2) {
  std::cout << "got an int instead of a vector" << std::endl;
}

template<typename S, typename T>
void append_to_vector(S v1, T v2) {
  std::cout << "got two non-vectors" << std::endl;
}

template<typename T, typename... A>
std::vector<T> concat(std::vector<T> v1, const A&... vr) {
    int unpack[] { (append_to_vector(v1, vr), 1)... };
    (void(unpack));
    return v1;
}


int main(){ 

  std::vector<std::vector<int>> VV;
  VV.emplace_back(std::initializer_list<int>{9, 9, 9, 9, 9, 9});
  VV.emplace_back(std::initializer_list<int>{1, 2, 3});
  VV.emplace_back(std::initializer_list<int>{5, 5, 5});

  std::cout <<  std::endl << std::endl << "Below we'll see indications of which templated function is being called during the unpacking in concat" << std::endl;
  auto bigV = concat( VV[0], 3, 4, VV[1], VV[2]);
  std::cout << std::endl << std::endl << "here's the size of the concatted vector: " << bigV.size();
  std::cout << std::endl << "Here's the element at index 6: " << bigV[6] << std::endl << std::endl;

}

