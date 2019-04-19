
#ifndef OPT_OPT_H_
#define OPT_OPT_H_


/** max f(w, n) with n fixed w;
 *  max g(W) with to w fixed n;
 *  g(W) = linear(W) ||W|| = 1;
 */

class Optimizer {
  Optimizer(Function func, Function grad_func, Constraint constraint);
  void Run();
};

class Variable {
  
};

class Function {
  
};

class Problem {
  Problem(Function func, Function grad_func, Constraint constraint);
};

class Constraint {
  
};

class Graident {

};









#endif
