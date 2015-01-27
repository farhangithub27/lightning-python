from numpy import ndarray, asarray

from lightning.types.base import Base
from lightning.types.decorators import viztype
from lightning.types.utils import array_to_im, mask_to_points, polygon_to_mask


@viztype
class Image(Base):
    _name = 'image'
    
    @staticmethod
    def clean(imagedata):
        """
        Display an array as an image.

        .. image:: image.png

        Parameters
        ----------
        imagedata : array-like
            Image as a two dimensional (grayscale) or three dimensional (RGB) array.
        """
        if asarray(imagedata).ndim not in set((2, 3)):
            raise Exception("Input must be two or three dimensional")

        outdict = [array_to_im(imagedata)]

        return {'images': outdict}
    
    def get_coords(self, return_type='bounds', dims=None):
        """
        Get data from polygons drawn on image.

        :param return_type:
        :return:
        """

        user_data = self.get_user_data()['settings']
        if 'coords' in user_data.keys():
            coords = user_data['coords']

            if return_type == 'bounds':
                return coords

            elif return_type == 'mask':
                if not dims:
                    raise Exception('Must provide image dimensions to return mask')
                return [polygon_to_mask(x, dims) for x in coords]

            elif return_type == 'points':
                if not dims:
                    raise Exception('Must provide image dimensions to return inner points')
                return [mask_to_points(polygon_to_mask(x, dims)) for x in coords]

            else:
                raise Exception('Option %s is not supported' % return_type)
        else:
            return []


@viztype
class Gallery(Base):

    _name = 'gallery'

    @staticmethod
    def clean(imagedata):
        """
        Display a collection of arrays as browsable images with thumbnails.

        .. image:: gallery.png

        Parameters
        ----------
        imagedata : array-like, or list of array-like
            Image or list of images as two dimensional (grayscale) or three dimensional (RGB) arrays.
        """

        if isinstance(imagedata, ndarray):
            imagedata = [imagedata]

        outdict = [array_to_im(im) for im in imagedata]

        return {'images': outdict}
