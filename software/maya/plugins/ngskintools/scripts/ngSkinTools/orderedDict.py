#
#    ngSkinTools
#    Copyright (c) 2009-2015 Viktoras Makauskas. 
#    All rights reserved.
#    
#    Get more information at 
#        http://www.ngskintools.com
#    
#    --------------------------------------------------------------------------
#
#    The coded instructions, statements, computer programs, and/or related
#    material (collectively the "Data") in these files are subject to the terms 
#    and conditions defined by
#    Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License:
#        http://creativecommons.org/licenses/by-nc-nd/3.0/
#        http://creativecommons.org/licenses/by-nc-nd/3.0/legalcode
#        http://creativecommons.org/licenses/by-nc-nd/3.0/legalcode.txt
#         
#    A copy of the license can be found in file 'LICENSE.txt', which is part 
#    of this source code package.
#    

'''
A compatibility fix for missing OrderedDict in pre-2014 mayas (running on python 2.6).

it's not a complete implementation of ordered dict, just the part needed for
specific usage in ngSkinTools. 
'''


class OrderedDict(object):
    
    def __init__(self,items):
        self.lookup = dict(items)
        self.items = items
        
    def keys(self):
        '''
        ordered sequence of keys
        '''
        return [item[0] for item in self.items]
    
    def __getitem__(self,index):
        return self.lookup[index]
