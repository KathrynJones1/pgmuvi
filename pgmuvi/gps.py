import numpy as np
import torch as t
import gpytorch as gpt
from gpytorch.means import ConstantMean, LinearMean
from gpytorch.kernels import SpectralMixtureKernel as SMK
from gpytorch.kernels import GridInterpolationKernel as GIK
from gpytorch.distributions import MultivariateNormal as MVN
from gpytorch.models import ExactGP



#### FIRST WE HAVE SOME Naive GPs
class TwoDSpectralMixtureGPModel(ExactGP):
    def __init__(self, train_x, train_y, likelihood, num_mixtures = 4):
        super(SpectralMixtureGPModel, self).__init__(train_x, train_y, likelihood)
        self.mean_module = ConstantMean()
        self.covar_module = SMK(ard_num_dims = 2, num_mixtures = num_mixtures)
        self.covar_module.initialize_from_data(train_x, train_y)


    def forward(self, x):
        mean_x = self.mean_module(x)
        covar_x = self.covar_module(x)
        return MVN(mean_x, covar_x)
        

class TwoDSpectralMixtureLinearMeanGPModel(ExactGP):
    def __init__(self, train_x, train_y, likelihood, num_mixtures = 4):
        super(SpectralMixtureLinearMeanGPModel, self).__init__(train_x, train_y, likelihood)
        self.mean_module = LinearMean()
        self.covar_module = SMK(ard_num_dims = 2, num_mixtures = num_mixtures)
        self.covar_module.initialize_from_data(train_x, train_y)


    def forward(self, x):
        mean_x = self.mean_module(x)
        covar_x = self.covar_module(x)
        return MVN(mean_x, covar_x)


#Now we define some that use KISS-GP/SKI to try to accelerate inference    
class TwoDSpectralMixtureKISSGPModel(ExactGP):
    def __init__(self, train_x, train_y, likelihood, num_mixtures = 4, grid_size = [5000,20]):
        super(SpectralMixtureKISSGPModel, self).__init__(train_x, train_y, likelihood)
        self.mean_module = ConstantMean()
        self.covar_module = GIK(SMK(ard_num_dims = 2, num_mixtures = num_mixtures), num_dims = 2, grid_size = grid_size
        )
        self.covar_module.initialize_from_data(train_x, train_y)


    def forward(self, x):
        mean_x = self.mean_module(x)
        covar_x = self.covar_module(x)
        return MVN(mean_x, covar_x)
        

class TwoDSpectralMixtureLinearMeanKISSGPModel(ExactGP):
    def __init__(self, train_x, train_y, likelihood, num_mixtures = 4, grid_size = [5000,20]):
        super(SpectralMixtureLinearMeanKISSGPModel, self).__init__(train_x, train_y, likelihood)
        self.mean_module = LinearMean()
        self.covar_module = GIK(SMK(ard_num_dims = 2, num_mixtures = num_mixtures), num_dims = 2, grid_size = grid_size
        )
        self.covar_module.initialize_from_data(train_x, train_y)


    def forward(self, x):
        mean_x = self.mean_module(x)
        covar_x = self.covar_module(x)
        return MVN(mean_x, covar_x)

#We can also implement sparse/variational GPs here