#include "../include/qureg.hpp"
#include "../include/gate_counter.hpp"
#include <iostream>
#include <cmath>

int main(int argc, char** argv) {

#ifndef INTELQS_HAS_MPI
    std::cout << "\nThis introductory code is thought to be run with MPI.\n"
        << "However the code will execute also without MPI.\n";
#endif

    iqs::mpi::Environment env(argc, argv);
    if (!env.IsUsefulRank()) return 0;

    int myid = env.GetStateRank();

    int num_qubits =  &&&

    iqs::QubitRegister<ComplexDP> psi(num_qubits);

    std::size_t index = 0;
    psi.Initialize("base", 0); &&&


psi.Print("Qubits: ");
if (myid == 0) std::cout << std::endl;


&&&


 if(myid==0){std::cout << "Qubits utilizados: " << num_qubits << std::endl;}
  


 }
 &&&
