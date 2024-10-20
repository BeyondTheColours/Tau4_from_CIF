# Tau4_from_CIF
Tool to calculate Tau4 geometric parameter from crystal structures.

Runs on the command line.
A python3 installation is required.

# How to use Tau4_from_CIF:
The symbol '$' represents a prompt in a terminal.

After downloading the Tau4_from_CIF.py file, use it in the command line as follows:

  $ python3 Tau4_from_CIF.py _path/to/yourCIF.cif_ _central_atom_

_central_atom_ is the atom around which Tau4 is to be calculated. This needs to be a valid atom in the .cif provided. For example, an atom named _Zn1_ in the .cif would be passed in like this:
  $ python3 Tau4_from_CIF.py _path/to/yourCIF.cif_ _Zn1_

Note that if the atom name is not spelled completely correctly the program will not be able to find it and so Tau4 will not be calculated.

The numeric value of Tau4 is printed out to the terminal when successful, or if an error preventing the calculation is encountered a message explaining the reason is printed to the terminal and the program exits.
