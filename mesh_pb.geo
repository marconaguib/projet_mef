// Projet MAIN 5 - Marco Naguib et Astrid Legay 

// Partie 1 : construction géométrique

// Constantes
   h = 0.1;
   L = 10;              
   l =8 ; 
   d = 0.5;
   

//Points
  // Pièces
    Point(1) = {0, 0, 0, h};  
    Point(2) = {L/3, 0, 0, h};
  	Point(3) = {L/3, l/6, 0, h};
  	Point(4) = {L/3+d, l/6, 0, h};
    Point(5) = {L/3+d, 0, 0, h};
    Point(6) = {((2*L)/3)-d, 0, 0, h};
    Point(7) = {((2*L)/3)-d, l/3, 0, h};
    Point(8) = {((2*L)/3), l/3, 0, h};
    Point(9) = {((2*L)/3), 0, 0, h};
    Point(10) = {L, 0, 0, h};
    Point(11) = {L,l/6 + 0.5,0,h};
    Point (12) = {((2*L)/3)+0.8, l/6+0.5,0,h}; 
    Point (13) = {((2*L)/3)+0.8, l/6+0.5+d,0,h};
    Point(14) = {L,l/6+0.5+d,0,h};
    Point (15) = {L,((2*l)/3)-d, 0, h};
    Point(16) = {L/3 , ((2*l)/3)-d,0,h};
    Point(17) = {L/3, ((2*l)/3),0,h} ; 
    Point(18) = {L, ((2*l)/3),0,h} ;
    Point(19) = {L,l,0,h}; 
    Point(20) ={L/3+d, l,0,h}; 
    Point(21) = {L/3+d, ((5*l)/6),0,h}; 
    Point(22) = {L/3, ((5*l)/6),0,h};
    Point(23) = {L/3, l,0,h};  
    Point(24) = {0,l,0,h}; 

    // Radiateurs

    Point(25) = {((2*L)/3)-d, l/3-0.3-1, 0, h};
    Point(26) = {((2*L)/3)-d, l/3-0.3, 0, h};
    Point (27) = {L-1,((2*l)/3)-d, 0, h};
    Point(28) = {L-2 , ((2*l)/3)-d,0,h};
    Point(29) = {0,l-1,0,h}; 
    Point(30) = {0,l-2,0,h}; 

    // Fenetres
    Point(31) = {L,l/6+1+d,0,h};
    Point (32) = {L,l/6+1+d+1, 0, h};
    Point(33) = {L-2,l,0,h}; 
    Point(34) ={L-3, l,0,h};
    Point(35) = {L/3-2, l,0,h};  
    Point(36) = {L/3-2-1,l,0,h}; 
    Point(37) = {0,l-5,0,h}; 
    Point(38) = {0,l-6,0,h}; 

// Lignes

// Pièces
Line(1) = {1,2}; 
Line(2) = {2,3}; 
Line(3) = {3,4};
Line(4) = {4,5};  
Line(5) = {5,6};
Line(6) = {6,25};
Line(32) = {26,7}; 
Line(7) = {7,8};
Line(8) = {8,9};
Line(9) = {9,10};
Line(10) = {10,11};
Line(11) = {11,12};
Line(12) = {12,13};
Line(13) = {13,14};
Line(14) = {14,31};
Line(33) = {32,15};
Line(15) = {15,27};
Line(38) = {28,16};
Line(16) = {16,17};
Line(17) = {17,18};
Line(18) = {18,19};
Line(19) = {19,33};
Line(34) = {34,20};
Line(20) = {20,21};
Line(21) = {21,22};
Line(22) = {22,23};
Line(23) = {23,35};
Line(35) = {36,24}; 
Line(24) = {24,29};
Line(36) = {30,37}; 
Line(37)= {38,1}; 

// Radiateurs
Line(25) = {25,26};
Line(26) = {27,28};
Line(27) = {29,30};

// Fenetres
Line(28) = {31,32};
Line(29) = {33,34};
Line(30) = {35,36};
Line(31) = {37,38};

// Autres
Curve Loop(1) = {1,2,3,4,5,6,25,32,7,8,9,10,11,12,13,14,28,33,15,26,38,16,17,18,19,29,34,20,21,22,23,30,35,24,27,36,31,37};   
Plane Surface(1) = {1}; 
Physical Line(1) = {1,2,3,4,5,6,32,7,8,9,10,11,12,13,14,33,15,38,16,17,18,19,34,20,21,22,23,35,24,36,37};  
Physical Line(2) = {25,26,27} ;
Physical Line(3) = {28,29,30,31} ;
Physical Surface(1) = {1,2,3};








