# -*- coding: utf-8 -*-
"""
Created on Tue May 14 18:05:59 2013

@author: jpeacock-pr
"""

import matplotlib.colors as colors
import numpy as np

#==============================================================================
# Make some color maps for plotting
#==============================================================================
#yellow to red
ptcmapdict = {'red':((0.0, 1.0, 1.0), 
                     (1.0, 1.0, 1.0)),

              'green':((0.0, 0.0, 1.0), 
                       (1.0, 0.0, 1.0)),

              'blue':((0.0, 0.0, 0.0), 
                      (1.0, 0.0, 0.0))}
                      
mt_yl2rd=colors.LinearSegmentedColormap('mt_yl2rd', ptcmapdict, 256)

#blue to yellow to red
skcmapdict = {'red':((0.0, 0.0, 0.0),
                     (.5, 1.0, 1.0),
                     (0.5, 0.0, 1.0),
                     (1.0, 1.0, 1.0)),
              'green':((0.0, 1.0, 0.0),
                       (.5, 1.0, 0.0),
                       (.5, 0.0, 1.0),
                       (1.0, 0.0, 1.0)),
              'blue':((0.0, 0.0, 1.0),
                      (.5, 0.0, 1.0),
                      (0.5, 0.1, 0.1),
                      (1.0, 0.1, 0.1))}
                      
mt_bl2yl2rd=colors.LinearSegmentedColormap('mt_bl2yl2rd', skcmapdict, 256)

#blue to white to red
skcmapdict2 = {'red':  ((0.0, 0.0, 0.0),
                        (0.25,0.0, 0.0),
                        (0.5, 0.8, 1.0),
                        (0.75,1.0, 1.0),
                        (1.0, 0.4, 1.0)),

               'green': ((0.0, 0.0, 0.0),
                         (0.25,0.0, 0.0),
                         (0.5, 0.9, 0.9),
                         (0.75,0.0, 0.0),
                         (1.0, 0.0, 0.0)),

               'blue':  ((0.0, 0.0, 0.4),
                         (0.25,1.0, 1.0),
                         (0.5, 1.0, 0.8),
                         (0.75,0.0, 0.0),
                         (1.0, 0.0, 0.0))}
                       
mt_bl2wh2rd=colors.LinearSegmentedColormap('mt_bl2wh2rd', skcmapdict2, 256)

            
#blue to white to red in segmented colors
mt_seg_bl2wh2rd = colors.ListedColormap(((0, 0, 1), (.5, .5, 1), (.75, .75, 1),
                                         (.9, .9, 1), (1, 1, 1), (1.0, .9, .9),
                                         (1, .75, .75), (1, .5, .5),(1, 0, 0)))

#white to blue
ptcmapdict3 = {'red':((0.0, 1.0, 1.0),
                      (1.0, 0.0, 0.0)),

               'green':((0.0, 1.0, 1.0),
                        (1.0, 0.0, 0.0)),

               'blue':((0.0, 1.0, 1.0),
                       (1.0, 1.0, 1.0))}
mt_wh2bl = colors.LinearSegmentedColormap('mt_wh2bl', ptcmapdict3, 256)

#white to orange
cmapdict_wh2or = {'red':((0.0, 1.0, 1.0),
                         (1.0, .95, 0.0)),

                  'green':((0.0, 1.0, 1.0),
                           (1.0, .45, .95)),

                  'blue':((0.0, 1.0, 1.0),
                          (1.0, 0, 0))}
mt_wh2or = colors.LinearSegmentedColormap('mt_wh2or', cmapdict_wh2or, 256)

#red to blue
rtcmapdict = {'red':((0.0, 0.0, 1.0),
                     (1.0, 0.0, 1.0)),

              'green':((0.0, 0.0, 0.0),
                       (1.0, 0.0, 0.0)),

              'blue':((0.0, 1.0, 0.0),
                      (1.0, 1.0, 0.0))}
mt_rd2bl = colors.LinearSegmentedColormap('mt_rd2bl', rtcmapdict, 256)

#blue to green to red
ptcmapdict4 = {'red':  ((0.0, 0.0, 0.0),
                        (0.25, 0.0, 0.0),
                        (0.5, 0.9, 1.0),
                        (0.75,1.0, 1.0),
                        (1.0, 0.45, 1.0)),

               'green': ((0.0, 0.0, 0.0),
                         (0.25, 0.5, 0.5),
                         (0.5, 1.0, 1.0),
                         (0.75,0.5, 0.5),
                         (1.0, 0.0, 0.0)),

              'blue':  ((0.0, 0.0, 0.45),
                        (0.25, 1.0, 1.0),
                        (0.5, 1.0, 0.9),
                        (0.75,0.0, 0.0),
                        (1.0, 0.0, 0.0))}
mt_bl2gr2rd = colors.LinearSegmentedColormap('mt_bl2gr2rd', ptcmapdict4, 256)

#red to green to blue
ptcmapdict4 = {'red':  ((0.0, 0.0, 0.45),
                        (0.25, 1.0, 1.0),
                        (0.5, 1.0, 0.9),
                        (0.75,0.0, 0.0),
                        (1.0, 0.0, 0.0)),

               'green': ((0.0, 0.0, 0.0),
                         (0.25, 0.5, 0.5),
                         (0.5, 1.0, 1.0),
                         (0.75,0.5, 0.5),
                         (1.0, 0.0, 0.0)),

              'blue':  ((0.0, 0.0, 0.0),
                        (0.25, 0.0, 0.0),
                        (0.5, 0.9, 1.0),
                        (0.75,1.0, 1.0),
                        (1.0, 0.45, 1.0))}
mt_rd2gr2bl = colors.LinearSegmentedColormap('mt_rd2gr2bl', ptcmapdict4, 256)


cmapdict = {'mt_yl2rd' : mt_yl2rd,
            'mt_bl2yl2rd' : mt_bl2yl2rd,
            'mt_wh2bl' : mt_wh2bl,
            'mt_rd2bl' : mt_rd2bl,
            'mt_bl2wh2rd' : mt_bl2wh2rd,
            'mt_seg_bl2wh2rd' : mt_seg_bl2wh2rd,
            'mt_bl2gr2rd' : mt_bl2gr2rd,
            'mt_rd2gr2bl' : mt_rd2gr2bl,
            'mt_wh2or' : mt_wh2or}
            
#make functions for getting the color from each map according to the variable
#cvar

def get_color(cvar,cmap):
    """
    gets the color to plot for the given color map
    
    """
    if cmap == 'mt_yl2rd':
        plot_color = get_mt_yl2rd(cvar)
        return plot_color
        
    elif cmap == 'mt_wh2bl':
        plot_color = get_mt_wh2bl(cvar)
        return plot_color
        
    elif cmap == 'mt_bl2wh2rd' or cmap=='mt_seg_bl2wh2rd':
        plot_color = get_mt_bl2wh2rd(cvar)
        return plot_color
        
    elif cmap == 'mt_bl2yl2rd':
        plot_color = get_mt_bl2yl2rd(cvar)
        return plot_color
        
    elif cmap == 'mt_bl2gr2rd':
        plot_color = get_mt_bl2gr2rd(cvar)
        return plot_color
        
    elif cmap == 'mt_rd2gr2bl':
        plot_color = get_mt_rd2gr2bl(cvar)
        return plot_color
    
    elif cmap == 'mt_wh2or':
        plot_color = get_mt_wh2or(cvar)
        return plot_color
        
    else:
        print 'Color map: {0} is not supported yet.'.format(cmap)
        
    
    
def get_mt_yl2rd(cvar):
    """
    gets color for the color map that goes from yellow to red
    
    """
    
    if cvar >= 1:
        plot_color = (1, 0, 0)
    elif cvar <= 0:
        plot_color = (1, 1, 0)
    else:
        plot_color = (1, 1-abs(cvar), 0.1)
        
    return plot_color
    
def get_mt_wh2bl(cvar):
    """
    gets color for the color map that goes from white to blue
    
    """
    
    if cvar >= 1:
        plot_color = (0, 0, 1)
    elif cvar <= 0:
        plot_color = (1, 1, 1)
    else:
        plot_color = (1-abs(cvar), 1-abs(cvar), 1)
        
    return plot_color
    
def get_mt_wh2or(cvar):
    """
    gets color for the color map that goes from white to orange
    
    """
    
    if cvar >= 1:
        plot_color = (1, .5, 0)
    elif cvar <= 0:
        plot_color = (1, 1, 1)
    else:
        plot_color = (1, abs(cvar)*.5+.5, abs(cvar))
        
    return plot_color
    
def get_mt_bl2wh2rd(cvar):
    """
    gets color for the color map that goes from blue to white to red
    
    """
    
    if cvar < 0 and cvar > -1:
        plot_color = (1+cvar, 1+cvar, 1)
    elif cvar <= -1:
        plot_color = (0, 0, 1)
    elif cvar >= 0 and cvar < 1:
        plot_color = (1, 1-cvar, 1-cvar)
    elif cvar >= 1:
        plot_color = (1, 0, 0)
        
    return plot_color
    
def get_mt_bl2yl2rd(cvar):
    """
    gets color for the color map that goes from blue to yellow to red
    
    """
    
    if cvar < 0 and cvar > -1:
        plot_color = (1+cvar, 1+cvar, -cvar)
    elif cvar <= -1:
        plot_color = (0, 0, 1)
    elif cvar >= 0 and cvar < 1:
        plot_color = (1, 1-cvar, .01)
    elif cvar >= 1:
        plot_color = (1, 0, 0)
        
    return plot_color
    
def get_mt_bl2gr2rd(cvar):
    """
    gets color for the color map that goes from blue to greenish to red
    
    """
    
    if cvar < 0 and cvar > -1:
        plot_color = (1+cvar, 1+cvar/2, 1)
    elif cvar <= -1:
        plot_color = (0, 0, 1)
    elif cvar >= 0 and cvar < 1:
        plot_color = (1, 1-cvar/2, 1-cvar)
    elif cvar >= 1:
        plot_color = (1, 0, 0)
        
    return plot_color
    
def get_mt_rd2gr2bl(cvar):
    """
    gets color for the color map that goes red to greenish to blue
    
    """
    
    if cvar < 0 and cvar > -1:
        plot_color = (1, 1+cvar/2, 1+cvar)
    elif cvar <= -1:
        plot_color = (1, 0, 0)
    elif cvar >= 0 and cvar < 1:
        plot_color = (1-cvar, 1-cvar/2, 1)
    elif cvar >= 1:
        plot_color = (0, 0, 1)
        
    return plot_color
    
def get_plot_color(colorx, comp, cmap, ckmin=None, ckmax=None, bounds=None):
    """
    gets the color for the given compnent, color array and cmap
    """
    
    
    #get face color info
    if comp == 'phimin' or comp == 'phimax' or comp == 'phidet' or \
       comp == 'ellipticity' or comp == 'geometric_mean':
        if ckmin is None or ckmax is None:
            raise IOError('Need to input min and max values for plotting')
        
        cvar = (colorx-ckmin)/(ckmax-ckmin)
        if cmap == 'mt_bl2wh2rd' or cmap == 'mt_bl2yl2rd' or \
           cmap == 'mt_bl2gr2rd' or cmap == 'mt_rd2gr2bl':
            cvar = 2*cvar-1
            
        return get_color(cvar, cmap)

    elif comp == 'skew' or comp == 'normalized_skew':
        cvar = 2*colorx/(ckmax-ckmin) 
        
        return get_color(cvar, cmap)
            
        
    elif comp == 'skew_seg' or comp == 'normalized_skew_seg':
        if bounds is None:
            raise IOError('Need to input bounds for segmented colormap')
        
        for bb in range(bounds.shape[0]):
            if colorx >= bounds[bb] and colorx < bounds[bb+1]:
                cvar = float(bounds[bb])/bounds.max()
                return get_color(cvar, cmap)
            
            #if the skew is extremely negative make it blue
            elif colorx < bounds[0]:
                cvar = -1.0
                return get_color(cvar, cmap)
            
            #if skew is extremely positive make it red
            elif colorx > bounds[-1]:
                cvar = 1.0
                return get_color(cvar, cmap)
        
    else:
        raise NameError('color key '+comp+' not supported')
    
def cmap_discretize(cmap, N):
    """Return a discrete colormap from the continuous colormap cmap.
      
         cmap: colormap instance, eg. cm.jet. 
         N: number of colors.
     
     Example
         x = resize(arange(100), (5,100))
         djet = cmap_discretize(cm.jet, 5)
         imshow(x, cmap=djet)
    """

    colors_i = np.concatenate((np.linspace(0, 1., N), (0.,0.,0.,0.)))
    colors_rgba = cmap(colors_i)
    indices = np.linspace(0, 1., N+1)
    cdict = {}
    for ki,key in enumerate(('red','green','blue')):
        cdict[key] = [(indices[i], colors_rgba[i-1,ki], colors_rgba[i,ki])
                       for i in xrange(N+1)]
    # Return colormap object.
    return colors.LinearSegmentedColormap(cmap.name + "_%d"%N, cdict, 1024)   

    


