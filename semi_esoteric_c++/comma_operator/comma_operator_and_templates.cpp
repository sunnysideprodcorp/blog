#include <iostream>

void f(){
  int k = 7;
  std::cout << "inside f " << std:: endl;
}

int main(){

  int i;
  i = (1, 2, (f()), 3);
  std::cout << i << std::endl;
  i = 1, 2, (f()), 3;
  std::cout << i << std::endl;
    
    
}
