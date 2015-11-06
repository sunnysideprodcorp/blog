
#include <algorithm>
#include <iostream>
#include <vector>
#include <string>
#include "NumericVector.h"
#include "VectorOfNumericVectors.h"
#include "Hist2D.h"
#include <chrono>

using namespace std::string_literals;

int MAX_N = 10000000;

//
// SUPPORTING FUNCTIONS
//

// used this timing method from http://stackoverflow.com/questions/2808398/easily-measure-elapsed-time
template<typename TimeT = std::chrono::microseconds>
struct measure
{
    template<typename F, typename ...Args>
    static typename TimeT::rep execution(F&& func, Args&&... args)
    {
        auto start = std::chrono::system_clock::now();
        std::forward<decltype(func)>(func)(std::forward<Args>(args)...);
        auto duration = std::chrono::duration_cast< TimeT> 
                            (std::chrono::system_clock::now() - start);
        return duration.count();
    }
};

// summary of recommended methods to implement something like std::cout << 5*"\n";
// from http://stackoverflow.com/questions/33572768/possible-to-overload-operator-to-multiple-an-int-and-a-char?noredirect=1#comment54926491_33572768

// method 1 user defined string converstion "_s operator
// method 2 piggy backs off defined operator* below and relies on explicit creation of std::string
std::string operator"" _s(const char* s) { return std::string(s); }
std::string operator"" _s(const char* s, std::size_t len) { return std::string(s, len); }
std::string operator* (int k, std::string s) {
    std::string t;
    for (unsigned int i = 0; i < k; ++i) {
      t += s;
    }
     
    return t;
}
std::string operator* (std::string s, int k) {
    std::string t;
    for (unsigned int i = 0; i < k; ++i) {
      t += s;
    }
     
    return t;
}

// method 3 define a struct to hold an int to fulfill requirement that operatore overloading only take place where at least one parameter is a user-defined type or enum
// this turns out to be the fastest
struct Mult { int value; };
std::string operator*(const Mult& m, const char* c){ 
  std::string t = "";
  for (int i = 0; i < m.value; ++i) {
    t += c;
    }
  return t;
};
std::string operator*( const char* c, const Mult& m){ 
  std::string t = "";
  for (int i = 0; i < m.value; ++i) {
    t += c;
    }
  return t;
};

// method 4 is not shown because it is simply using string literals "\n"s as available in C++ 14

// method 5 define a repeat function
std::string repeat (std::size_t n, std::string s) {
  std::string t = "";
  for(std::size_t i = 0; i < n; ++i) {
    t += s;
  }
  return t;
}

//
// FUNCTION OBJECTS TO CALL WITH TIMING FUNCTION
//

// user defined string converstion "_s operator
struct op1 {
  void operator()() {
    for(int i = 0; i < MAX_N; i++){
      auto s = 5*"n"_s;
    }
  }
};

// operator overloading and explicit string conversion
struct op2 {
  void operator()() {
    for(int i = 0; i < MAX_N; i++){
      auto s = 5 * std::string("n"); 
    }
  }
};

// storing int inside a struct to circumvent standard about not overlapping on built in types
struct op3 {
  void operator()(){
    Mult v;
    v.value = 5;
    for(int i = 0; i < MAX_N; i++){      
      auto s = v * "n"; 
    }
  }
};

// using c++ 14
struct op4 {
  void operator()() {
    for(int i = 0; i < MAX_N; i++){
      auto s = 5*"n"s;
    }
  }
};

// using custom function repeat
struct op5 {
  void operator()() {
    for(int i = 0; i < MAX_N; i++){
      auto s = repeat(5, "s");
    }
  }
};


int main()
{
  std::cout << measure<>::execution(op1()) << std::endl;
  std::cout << measure<>::execution(op2()) << std::endl;
  std::cout << measure<>::execution(op3()) << std::endl; 
  std::cout << measure<>::execution(op4()) << std::endl;
  std::cout << measure<>::execution(op5()) << std::endl;

}
