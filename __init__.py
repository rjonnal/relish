import pickle,os,sys

cache_directory_default = os.path.join(os.path.abspath(''),'.relish_cache')

def fix_filename(filename,cache_directory):
    # make sure we're just using the basename, in case caller has given the
    # full path:
    filename = os.path.split(filename)[1]
    
    # add the cache path:
    filename = os.path.join(cache_directory,filename)

    return filename

def save(filename,obj,cache_directory=cache_directory_default,protocol=pickle.HIGHEST_PROTOCOL):
    
    try:
        os.mkdir(cache_directory)
    except Exception as e:
        pass
    
    filename = fix_filename(filename,cache_directory)
    
    # serialize and dump, catching errors
    # sys.exit on error since we don't want execution to complete on
    # failed saves
    try:
        with open(filename,'wb') as fid:
            pickle.dump(obj,fid,protocol=protocol)
    except pickle.PicklingError as pe:
        print('PicklingError / unserializable data',pe)
        sys.exit()
    except RecursionError as re:
        print('RecursionError / data structure too deeply recursive',re)
        sys.exit()
    except Exception as e:
        print(e)
        sys.exit()
        

def load(filename,cache_directory=cache_directory_default,protocol=pickle.HIGHEST_PROTOCOL):

    filename = fix_filename(filename,cache_directory)
    # raise exceptions, but don't exit
    try:
        with open(filename,'rb') as fid:
            obj = pickle.load(fid)
    except pickle.UnpicklingError as ue:
        raise ue
    except FileNotFoundError as fnfe:
        raise fnfe
    return obj
