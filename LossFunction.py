import torch 
import torch.nn as nn 
from torch.autograd import Variable
import torch.autograd as autograd




def original_gan_loss(target, is_real, mode = 'D'):

	assert mode in ['D', 'G'] "There are only two modes in training GAN"


	real = Variable(Tensor(target.shape[0], 1).fill_(1.0), requires_grad=False)
	fake = Variable(Tensor(target.shape[0], 1).fill_(0.0), requires_grad=False)
	loss = None 
	criterion = torch.nn.BCELoss()

	if mode == 'D':
		if is_real:
			loss = criterion(target, real)
		else:
			loss = criterion(target, fake)

	else:
		assert is_real == False "The generator always generates fake targets and tries to fool the discriminator."
		loss = criterion(target, real)

	return loss 



def hinge_gan_loss(target, is_real, mode = 'D'):


	assert mode in ['D', 'G'] "There are only two modes in training GAN"

	loss = None

	if mode == 'D':
		zeros = Variable(Tensor(target.shape[0], 1).fill_(0.0), requires_grad=False)
		if is_real: 
			loss = torch.min(zeros, -1 + target)
			loss = -torch.mean(loss)

		else:
			loss = torch.min(zeros, -1 - target)
			loss = -torch.mean(loss)

	else:
		loss = -torch.mean(target)


	return loss 


def w_gan_loss(fake_target, real_target = None, mode = 'D'):
	
	assert mode in ['D', 'G']


	loss = None
	
	if mode == 'D':
		assert real_target is not None "The total mean of fake and real targets"

		loss = torch.mean(fake_target) - torch.mean(real_target)

	else:
		assert real_target == None 

		loss = -torch.mean(fake_target)

	return loss


def compute_gradient_penalty(discriminator, real_images, fake_images):
	
	"""Calculates the gradient penalty loss for WGAN GP"""
	# Random weight term for interpolation between real and fake images
	
	alpha = Tensor(np.random.random((real_images.size(0), 1, 1, 1)))
	
	# Get random interpolation between real and fake images
	
	interpolates = (alpha * real_images + ((1 - alpha) * fake_images)).requires_grad_(True)
	d_interpolates = discriminator(interpolates)
	fake = Variable(Tensor(real_images.shape[0], 1).fill_(1.0), requires_grad=False)
	
	# Get gradient w.r.t. interpolates
	
	gradients = autograd.grad(
		outputs= d_interpolates,
		inputs= interpolates,
		grad_outputs= fake,
		create_graph= True,
		retain_graph= True,
		only_inputs= True,
	)[0]

	gradients = gradients.view(gradients.size(0), -1)
	gradient_penalty = ((gradients.norm(2, dim=1) - 1) ** 2).mean()
	return gradient_penalty


def reconstruction_loss(original_image, generated_image):
	return nn.L1Loss(original_image, generated_image)




def feature_map_loss(discriminator, x, y): 
	pass 


def perceptual_loss(discriminator, x, y):
	pass 

