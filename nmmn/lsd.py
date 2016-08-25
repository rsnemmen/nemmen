"""
LSD operations = lists, sets, dictionaries (and arrays)
=========================================================
"""

import numpy
import scipy


def cmset_and(x,y):
	"""
Usage:

>>> cmset_and(x,y)

returns the index of the elements of array x which are also present in the
array y. 

This is equivalent to using the IDL command

>>> botha=cmset_op(namea, 'AND', nameb, /index)

i.e. performs the same thing as the IDL routine cmset_op from
http://cow.physics.wisc.edu/~craigm/idl/idl.html.
	"""
	
	idel=[]	# list of indexes of x elements which are also in y
	i=0
	for xx in x:
		if xx in y: idel.append(i)
		i=i+1
		
	return idel




def cmsetsort_and(x,y):
	"""
Usage:

>>> cmsetsort_and(x,y)

returning the index of the elements of array x which are also present in the
array y. 

The resulting elements have the same order as the ones in y. For 
instance, if you run

>>> i=cmsetsort_and(x,y)
>>> x[i]==y

will return an array of True, whereas if you used instead cmset_and it is
not guaranteed that all elements would match in x[i] and y.

Inherited from :func:`nemmen.cmset_and`.
	"""
	
	idel=[]	# list of indexes of x elements which are also in y
	i=0
	for yy in y:
		i=numpy.where(x==yy)
		idel.append( i[0].item() )
		
	return idel
	



def cmset_not(x,y):
	"""
Usage:
>>> cmset_not(x,y)
returning the index of the elements of array x which are not present in the
array y. 

This is equivalent to using the IDL command
SET = CMSET_OP(A, 'AND', /NOT2, B, /INDEX)   ; A but not B
i.e. performs the same thing as the IDL routine cmset_op from
http://cow.physics.wisc.edu/~craigm/idl/idl.html.
	"""
	
	idel=[]	# list of indexes of x elements which NOT in y
	i=0
	for xx in x:
		if xx not in y: idel.append(i)
		i=i+1
		
	return idel


	
def delnan(x):
	"""
Remove nan elements from the array.
	"""
	# Index of nan elements
	i=numpy.where(numpy.isnan(x)==True)
	
	# Removes the nan elements
	return numpy.delete(x,i)
	


def delweird(x):
	"""
Remove nan or inf elements from the array.
	"""
	# Index of nan elements
	i=numpy.where( (numpy.isnan(x)==True) | (numpy.isinf(x)==True) )
	
	# Removes the nan elements
	return numpy.delete(x,i)


	
	
def search(xref, x):
	"""
Search for the element in an array x with the value nearest xref.
Piece of code based on http://stackoverflow.com/questions/2566412/find-nearest-value-in-numpy-array

>>> i=search(xref, x)

:param xref: input number, array or list of reference values
:param x: input array
:returns: index of the x-elements with values nearest to xref:
	"""
	if numpy.size(xref)==1:
		i=(numpy.abs(x-xref)).argmin()
	else:
		i=[]

		for y in xref:
			i.append( (numpy.abs(x-y)).argmin() )
	        
	return i
	


def sortindex(x,**kwargs):
	"""
Returns the list of indexes, ordered according to the numerical value of each 
element of x.

:param x: input array or list.
:returns: list of element indexes.
	"""
	f=lambda i: x[i]

	return sorted( range(numpy.size(x)) , key=f,**kwargs)
	



def norm(x1,x2=None):
	"""
Normalizes x1. If also given as input x2, then normalizes x1 to x2.

:param x1: input array
:param x2: optional
:returns: normalized x1
	"""
	if x2==None:
		return x1/x1.max()
	else:
		return x1*x2.max()/x1.max()





def uarray(x,errx):
	"""
With the new releases of the uncertainties and astropy.io.ascii (0.2.3, the
replacement of asciitable), if I try to create an uncertainties array with
the column of a table imported with ascii I run into trouble. For instance, 
if I use the sequence of commands below:

>>> import astropy.io.ascii as asciitable
>>> raff= asciitable.read('data/rafferty06.dat')
>>> m,errm=raff['mass'],raff['errm']
>>> mass=unumpy.uarray(m,errm)
>>> x=0.2*mass

I get the error message: 

>>> TypeError: unsupported operand type(s) for *: 'float' and 'Column'

which I can only assume is due to the new way ascii handles tables.

I created this method to use as a replacement for unumpy.uarray that handles
the tables created with astropy.io.ascii.

Usage is the same as uncertainties.unumpy.uarray.

:type x,errx: arrays created with astropy.io.ascii.
:returns: uncertainties array.
	"""
	import uncertainties.unumpy as unumpy

	x=numpy.array(x)
	errx=numpy.array(errx)

	return unumpy.uarray(x,errx)






	
def bootstrap(v):
	"""
Constructs Monte Carlo simulated data set using the
Bootstrap algorithm.                                                                                   

Usage:

>>> bootstrap(x)

where x is either an array or a list of arrays. If it is a
list, the code returns the corresponding list of bootstrapped 
arrays assuming that the same position in these arrays map the 
same "physical" object.

Rodrigo Nemmen, http://goo.gl/8S1Oo
	"""
	if type(v)==list:
		vboot=[]	# list of boostrapped arrays
		n=v[0].size
		iran=scipy.random.randint(0,n,n)	# Array of random indexes
		for x in v:	vboot.append(x[iran])
	else:	# if v is an array, not a list of arrays
		n=v.size
		iran=scipy.random.randint(0,n,n)	# Array of random indexes
		vboot=v[iran]
	
	return vboot
	




