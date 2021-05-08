class Image:
  def __init__(self, data):
    self.data = data
    
  def splatAtPixCoord(self, im, location=[0, 0]):
    is_int = self._is_int;
        selftype = self.dtype;
        region0 = [location[0], (location[0]+im.data.shape[0])];
        region1 = [location[1], (location[1]+im.data.shape[1])];
        if(im.n_channels<4):
            self.data[region0[0]:region0[1], region1[0]:region1[1],:]=im.data;
            return;
        if(im.n_channels == 4):
            alphamap = np.moveaxis(np.tile(im._pixels_float[:, :, 3], (3, 1, 1)), [0], [2]);

            blenda = (im._pixels_float[:, :, :3]) * alphamap + self._pixels_float[region0[0]:region0[1], region1[0]:region1[1],:]*(1.0 - alphamap);
            if(is_int):
                blenda = (blenda*255).astype(selftype);
            self.data[region0[0]:region0[1], region1[0]:region1[1], :] = blenda;