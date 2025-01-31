import numpy as np
import torch as t
import gpytorch as gpt
from gpytorch.means import ConstantMean, LinearMean
from gpytorch.kernels import SpectralMixtureKernel as SMK
from gpytorch.kernels import GridInterpolationKernel as GIK
from gpytorch.distributions import MultivariateNormal as MVN
from gpytorch.models import ExactGP, ApproximateGP



#### FIRST WE HAVE SOME Naive GPs
class SpectralMixtureGPModel(ExactGP):
    ''' A one-dimensional GP model using a spectral mixture kernel

    A Gaussian Process which uses a Spectral Mixture Kernel to model the Power 
    Spectral Density of the covariance matrix as a Gaussian Mixture Model. 
    This model assumes the mean is constant.

    Parameters
    ----------
    train_x : Tensor
        The data for the independent variable (typically timestamps)
    train_y : Tensor
        The data for the dependent variable (typically flux)
    likelihood : a Likelihood object or subclass
        The likelihood that will be used to evaluate the model
    num_mixtures : int
        Number of components in the Mixture Model. More mixtures gives more
        flexibility, but more hyperparameters and more complex inference

    Examples
    --------


    Notes
    ------

    

    '''
    def __init__(self, train_x, train_y, likelihood, num_mixtures = 4):
        super(SpectralMixtureGPModel, self).__init__(train_x, train_y, likelihood)
        self.mean_module = ConstantMean()
        self.covar_module = SMK(num_mixtures = num_mixtures)
        self.covar_module.initialize_from_data(train_x, train_y)

        #Now we alias the covariance kernel so that we can exploit the same object properties in different classes with different kernel structure
        #Will turn this into an @property at some point.
        self.sci_kernel = self.covar_module


    def forward(self, x):
        mean_x = self.mean_module(x)
        covar_x = self.covar_module(x)
        return MVN(mean_x, covar_x)

class SpectralMixtureLinearMeanGPModel(ExactGP):
    ''' A one-dimensional GP model using a spectral mixture kernel

    A Gaussian Process which uses a Spectral Mixture Kernel to model the Power 
    Spectral Density of the covariance matrix as a Gaussian Mixture Model. 
    This model assumes the mean is a linear function.

    Parameters
    ----------
    train_x : Tensor
        The data for the independent variable (typically timestamps)
    train_y : Tensor
        The data for the dependent variable (typically flux)
    likelihood : a Likelihood object or subclass
        The likelihood that will be used to evaluate the model
    num_mixtures : int
        Number of components in the Mixture Model. More mixtures gives more
        flexibility, but more hyperparameters and more complex inference

    Examples
    --------


    Notes
    ------

    

    '''
    def __init__(self, train_x, train_y, likelihood, num_mixtures = 4):
        super(SpectralMixtureLinearMeanGPModel, self).__init__(train_x, train_y, likelihood)
        self.mean_module = LinearMean()
        self.covar_module = SMK(num_mixtures = num_mixtures)
        self.covar_module.initialize_from_data(train_x, train_y)

        #Now we alias the covariance kernel so that we can exploit the same object properties in different classes with different kernel structure
        #Will turn this into an @property at some point.
        self.sci_kernel = self.covar_module


    def forward(self, x):
        mean_x = self.mean_module(x)
        covar_x = self.covar_module(x)
        return MVN(mean_x, covar_x)

class TwoDSpectralMixtureGPModel(ExactGP):
    ''' A two-dimensional GP model using a spectral mixture kernel

    A Gaussian Process which uses a Spectral Mixture Kernel to model the Power 
    Spectral Density of the covariance matrix as a Gaussian Mixture Model. 
    This model assumes the mean is constant. It supports datasets with two 
    independent variables (e.g. time and wavelength). 

    Parameters
    ----------
    train_x : Tensor
        The data for the independent variable (typically timestamps and wavelengths)
    train_y : Tensor
        The data for the dependent variable (typically flux)
    likelihood : a Likelihood object or subclass
        The likelihood that will be used to evaluate the model
    num_mixtures : int
        Number of components in the Mixture Model. More mixtures gives more
        flexibility, but more hyperparameters and more complex inference

    Examples
    --------


    Notes
    ------

    

    '''
    def __init__(self, train_x, train_y, likelihood, num_mixtures = 4):
        super(TwoDSpectralMixtureGPModel, self).__init__(train_x, train_y, likelihood)
        self.mean_module = ConstantMean()
        self.covar_module = SMK(ard_num_dims = 2, num_mixtures = num_mixtures)
        self.covar_module.initialize_from_data(train_x, train_y)

        #Now we alias the covariance kernel so that we can exploit the same object properties in different classes with different kernel structure
        #Will turn this into an @property at some point.
        self.sci_kernel = self.covar_module


    def forward(self, x):
        mean_x = self.mean_module(x)
        covar_x = self.covar_module(x)
        return MVN(mean_x, covar_x)
        

class TwoDSpectralMixtureLinearMeanGPModel(ExactGP):
    ''' A two-dimensional GP model using a spectral mixture kernel

    A Gaussian Process which uses a Spectral Mixture Kernel to model the Power 
    Spectral Density of the covariance matrix as a Gaussian Mixture Model. 
    This model assumes the mean is a linear function.  It supports datasets 
    with two independent variables (e.g. time and wavelength). 

    Parameters
    ----------
    train_x : Tensor
        The data for the independent variable (typically timestamps and wavelengths)
    train_y : Tensor
        The data for the dependent variable (typically flux)
    likelihood : a Likelihood object or subclass
        The likelihood that will be used to evaluate the model
    num_mixtures : int
        Number of components in the Mixture Model. More mixtures gives more
        flexibility, but more hyperparameters and more complex inference

    Examples
    --------


    Notes
    ------

    

    '''
    def __init__(self, train_x, train_y, likelihood, num_mixtures = 4):
        super(TwoDSpectralMixtureLinearMeanGPModel, self).__init__(train_x, train_y, likelihood)
        self.mean_module = LinearMean()
        self.covar_module = SMK(ard_num_dims = 2, num_mixtures = num_mixtures)
        self.covar_module.initialize_from_data(train_x, train_y)

        #Now we alias the covariance kernel so that we can exploit the same object properties in different classes with different kernel structure
        #Will turn this into an @property at some point.
        self.sci_kernel = self.covar_module


    def forward(self, x):
        mean_x = self.mean_module(x)
        covar_x = self.covar_module(x)
        return MVN(mean_x, covar_x)


#Now we define some that use KISS-GP/SKI to try to accelerate inference
class SpectralMixtureKISSGPModel(ExactGP):
    ''' A one-dimensional GP model using a spectral mixture kernel

    A Gaussian Process which uses a Spectral Mixture Kernel to model the Power 
    Spectral Density of the covariance matrix as a Gaussian Mixture Model. 
    This model assumes the mean is constant. It uses the Kernel interpolation 
    for scalable structured Gaussian processes (KISS-GP) approximation to 
    enable scaling to much larger datasets. This means it becomes effective 
    when your dataset exceeds ~10,000 entries; for smaller datasets, the 
    overhead of interpolation is typically not worth the effort.

    Parameters
    ----------
    train_x : Tensor
        The data for the independent variable (typically timestamps)
    train_y : Tensor
        The data for the dependent variable (typically flux)
    likelihood : a Likelihood object or subclass
        The likelihood that will be used to evaluate the model
    num_mixtures : int
        Number of components in the Mixture Model. More mixtures gives more
        flexibility, but more hyperparameters and more complex inference
    grid_size : int
        The number of points to use in the kernel interpolation grid.

    Examples
    --------


    Notes
    ------

    

    '''
    def __init__(self, train_x, train_y, likelihood, num_mixtures = 4, grid_size = 2000):
        super(SpectralMixtureKISSGPModel, self).__init__(train_x, train_y, likelihood)
        if not grid_size:
            grid_size = gpt.utils.grid.choose_grid_size(train_x,1.0)
            print("Using a grid of size ", grid_size," for SKI")
        grid_bounds = [[t.min(train_x), t.max(train_x)]]
        self.mean_module = ConstantMean()
        self.covar_module = GIK(SMK(num_mixtures = num_mixtures), grid_size = grid_size, num_dims=1, grid_bounds = grid_bounds
        )

        self.covar_module.base_kernel.initialize_from_data(train_x, train_y)

        self.sci_kernel = self.covar_module.base_kernel
        #self.covar_module.base_kernel.initialize_from_data(train_x, train_y)


    def forward(self, x):
        mean_x = self.mean_module(x)
        covar_x = self.covar_module(x)
        return MVN(mean_x, covar_x)
        

class SpectralMixtureLinearMeanKISSGPModel(ExactGP):
    ''' A one-dimensional GP model using a spectral mixture kernel

    A Gaussian Process which uses a Spectral Mixture Kernel to model the Power 
    Spectral Density of the covariance matrix as a Gaussian Mixture Model. 
    This model assumes the mean is a linear function. It uses the Kernel 
    interpolation for scalable structured Gaussian processes (KISS-GP) 
    approximation to enable scaling to much larger datasets. This means it 
    becomes effective when your dataset exceeds ~10,000 entries; for smaller 
    datasets, the overhead of interpolation is typically not worth the effort.

    Parameters
    ----------
    train_x : Tensor
        The data for the independent variable (typically timestamps)
    train_y : Tensor
        The data for the dependent variable (typically flux)
    likelihood : a Likelihood object or subclass
        The likelihood that will be used to evaluate the model
    num_mixtures : int
        Number of components in the Mixture Model. More mixtures gives more
        flexibility, but more hyperparameters and more complex inference
    grid_size : int
        The number of points to use in the kernel interpolation grid.

    Examples
    --------


    Notes
    ------

    

    '''
    def __init__(self, train_x, train_y, likelihood, num_mixtures = 4, grid_size = 2000):
        super(SpectralMixtureLinearMeanKISSGPModel, self).__init__(train_x, train_y, likelihood)
        self.mean_module = LinearMean()
        self.covar_module = GIK(SMK(num_mixtures = num_mixtures), grid_size = grid_size
        )
        self.covar_module.base_kernel.initialize_from_data(train_x, train_y)

        #Now we alias the covariance kernel so that we can exploit the same object properties in different classes with different kernel structure
        #Will turn this into an @property at some point.
        self.sci_kernel = self.covar_module


    def forward(self, x):
        mean_x = self.mean_module(x)
        covar_x = self.covar_module(x)
        return MVN(mean_x, covar_x)

    
class TwoDSpectralMixtureKISSGPModel(ExactGP):
    ''' A two-dimensional GP model using a spectral mixture kernel

    A Gaussian Process which uses a Spectral Mixture Kernel to model the Power 
    Spectral Density of the covariance matrix as a Gaussian Mixture Model. 
    This model assumes the mean is constant. It supports datasets with two 
    independent variables (e.g. time and wavelength). It uses the Kernel 
    interpolation for scalable structured Gaussian processes (KISS-GP) 
    approximation to enable scaling to much larger datasets. This means it 
    becomes effective when your dataset exceeds ~10,000 entries; for smaller 
    datasets, the overhead of interpolation is typically not worth the effort.

    Parameters
    ----------
    train_x : Tensor
        The data for the independent variable (typically timestamps)
    train_y : Tensor
        The data for the dependent variable (typically flux)
    likelihood : a Likelihood object or subclass
        The likelihood that will be used to evaluate the model
    num_mixtures : int
        Number of components in the Mixture Model. More mixtures gives more
        flexibility, but more hyperparameters and more complex inference
    grid_size : (2x1) iterable of ints
        The number of points to use in the kernel interpolation grid, with one value per dimension.

    Examples
    --------


    Notes
    ------

    

    '''
    def __init__(self, train_x, train_y, likelihood, num_mixtures = 4, grid_size = [5000,20]):
        super(SpectralMixtureKISSGPModel, self).__init__(train_x, train_y, likelihood)
        self.mean_module = ConstantMean()
        self.covar_module = GIK(SMK(ard_num_dims = 2, num_mixtures = num_mixtures), num_dims = 2, grid_size = grid_size
        )
        self.covar_module.base_kernel.initialize_from_data(train_x, train_y)

        #Now we alias the covariance kernel so that we can exploit the same object properties in different classes with different kernel structure
        #Will turn this into an @property at some point.
        self.sci_kernel = self.covar_module


    def forward(self, x):
        mean_x = self.mean_module(x)
        covar_x = self.covar_module(x)
        return MVN(mean_x, covar_x)
        

class TwoDSpectralMixtureLinearMeanKISSGPModel(ExactGP):
    ''' A two-dimensional GP model using a spectral mixture kernel

    A Gaussian Process which uses a Spectral Mixture Kernel to model the Power 
    Spectral Density of the covariance matrix as a Gaussian Mixture Model. 
    This model assumes the mean is a linear function. It supports datasets 
    with two independent variables (e.g. time and wavelength). It uses the 
    Kernel interpolation for scalable structured Gaussian processes (KISS-GP) 
    approximation to enable scaling to much larger datasets. This means it 
    becomes effective when your dataset exceeds ~10,000 entries; for smaller 
    datasets, the overhead of interpolation is typically not worth the effort.

    Parameters
    ----------
    train_x : Tensor
        The data for the independent variable (typically timestamps)
    train_y : Tensor
        The data for the dependent variable (typically flux)
    likelihood : a Likelihood object or subclass
        The likelihood that will be used to evaluate the model
    num_mixtures : int
        Number of components in the Mixture Model. More mixtures gives more
        flexibility, but more hyperparameters and more complex inference
    grid_size : (2x1) iterable of ints
        The number of points to use in the kernel interpolation grid, with one value per dimension.

    Examples
    --------


    Notes
    ------

    

    '''
    def __init__(self, train_x, train_y, likelihood, num_mixtures = 4, grid_size = [5000,20]):
        super(TwoDSpectralMixtureLinearMeanKISSGPModel, self).__init__(train_x, train_y, likelihood)
        self.mean_module = LinearMean()
        self.covar_module = GIK(SMK(ard_num_dims = 2, num_mixtures = num_mixtures), num_dims = 2, grid_size = grid_size
        )
        self.covar_module.base_kernel.initialize_from_data(train_x, train_y)

        #Now we alias the covariance kernel so that we can exploit the same object properties in different classes with different kernel structure
        #Will turn this into an @property at some point.
        self.sci_kernel = self.covar_module


    def forward(self, x):
        mean_x = self.mean_module(x)
        covar_x = self.covar_module(x)
        return MVN(mean_x, covar_x)


from gpytorch.variational import CholeskyVariationalDistribution
from gpytorch.variational import VariationalStrategy
    
#We can also implement sparse/variational GPs here
class SparseSpectralMixtureGPModel(ApproximateGP):
    ''' A one-dimensional GP model using a spectral mixture kernel

    A longer description goes here

    Parameters
    ----------
    train_x : Tensor
        The data for the independent variable (typically timestamps)
    train_y : Tensor
        The data for the dependent variable (typically flux)
    likelihood : a Likelihood object or subclass
        The likelihood that will be used to evaluate the model
    num_mixtures : int
        Number of components in the Mixture Model. More mixtures gives more
        flexibility, but more hyperparameters and more complex inference

    Examples
    --------


    Notes
    ------

    

    '''
    def __init__(self, train_x, train_y, likelihood, num_mixtures = 4):
        variational_distribution = CholeskyVariationalDistribution(inducing_points.size(0))
        variational_strategy = VariationalStrategy(self, inducing_points, variational_distribution, learn_inducing_locations=True)
        super(SpectralMixtureGPModel, self).__init__(variational_strategy)
        #super(SpectralMixtureGPModel, self).__init__(train_x, train_y, likelihood)
        self.mean_module = ConstantMean()
        self.covar_module = SMK(num_mixtures = num_mixtures)
        self.covar_module.initialize_from_data(train_x, train_y)

        #Now we alias the covariance kernel so that we can exploit the same object properties in different classes with different kernel structure
        #Will turn this into an @property at some point.
        self.sci_kernel = self.covar_module


    def forward(self, x):
        mean_x = self.mean_module(x)
        covar_x = self.covar_module(x)
        return MVN(mean_x, covar_x)

class SparseSpectralMixtureLinearMeanGPModel(ExactGP):
    ''' A one-dimensional GP model using a spectral mixture kernel

    A longer description goes here

    Parameters
    ----------
    train_x : Tensor
    train_y : Tensor
    likelihood : a Likelihood object or subclass
    num_mixtures : int

    Examples
    --------


    Notes
    ------

    

    '''
    def __init__(self, train_x, train_y, likelihood, num_mixtures = 4):
        super(SpectralMixtureLinearMeanGPModel, self).__init__(train_x, train_y, likelihood)
        self.mean_module = LinearMean()
        self.covar_module = SMK(num_mixtures = num_mixtures)
        self.covar_module.initialize_from_data(train_x, train_y)

        #Now we alias the covariance kernel so that we can exploit the same object properties in different classes with different kernel structure
        #Will turn this into an @property at some point.
        self.sci_kernel = self.covar_module


    def forward(self, x):
        mean_x = self.mean_module(x)
        covar_x = self.covar_module(x)
        return MVN(mean_x, covar_x)

class SparseTwoDSpectralMixtureGPModel(ExactGP):
    ''' A one-dimensional GP model using a spectral mixture kernel

    A longer description goes here

    Parameters
    ----------
    train_x : Tensor
    train_y : Tensor
    likelihood : a Likelihood object or subclass
    num_mixtures : int

    Examples
    --------


    Notes
    ------

    

    '''
    def __init__(self, train_x, train_y, likelihood, num_mixtures = 4):
        super(TwoDSpectralMixtureGPModel, self).__init__(train_x, train_y, likelihood)
        self.mean_module = ConstantMean()
        self.covar_module = SMK(ard_num_dims = 2, num_mixtures = num_mixtures)
        self.covar_module.initialize_from_data(train_x, train_y)

        #Now we alias the covariance kernel so that we can exploit the same object properties in different classes with different kernel structure
        #Will turn this into an @property at some point.
        self.sci_kernel = self.covar_module


    def forward(self, x):
        mean_x = self.mean_module(x)
        covar_x = self.covar_module(x)
        return MVN(mean_x, covar_x)
        

class SparseTwoDSpectralMixtureLinearMeanGPModel(ExactGP):
    ''' A one-dimensional GP model using a spectral mixture kernel

    A longer description goes here

    Parameters
    ----------
    train_x : Tensor
    train_y : Tensor
    likelihood : a Likelihood object or subclass
    num_mixtures : int

    Examples
    --------


    Notes
    ------

    

    '''
    def __init__(self, train_x, train_y, likelihood, num_mixtures = 4):
        super(TwoDSpectralMixtureLinearMeanGPModel, self).__init__(train_x, train_y, likelihood)
        self.mean_module = LinearMean()
        self.covar_module = SMK(ard_num_dims = 2, num_mixtures = num_mixtures)
        self.covar_module.initialize_from_data(train_x, train_y)

        #Now we alias the covariance kernel so that we can exploit the same object properties in different classes with different kernel structure
        #Will turn this into an @property at some point.
        self.sci_kernel = self.covar_module


    def forward(self, x):
        mean_x = self.mean_module(x)
        covar_x = self.covar_module(x)
        return MVN(mean_x, covar_x)
