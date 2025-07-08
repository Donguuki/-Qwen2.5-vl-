import os

pic = 'pic'
for i,filename in enumerate(os.listdir(pic)):
    file = os.path.join(pic,filename)
    new_name = os.path.join(pic,'{}.png'.format(i))
    os.rename(file,new_name)
    
        
