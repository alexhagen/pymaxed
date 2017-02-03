class pymaxed(object):
    def __init__(self, bs_sizes=None, bs_crs=None, response_function=None,
                 output_fname='outp', guess_spectrum=None, maxE=20.,
                 chi2=5., T=1.0, eta=0.85, dsE=(1,1), scaleDS=1, maxedscale=1):
        with open(inp_fname, 'w') as f:
            # first find the file with measured data in ibu format
            self.ibu = ibu_file(fname, bs_sizes, bs_crs)
            f.write(self.ibu)
            # then create the response function file in fmt format
            self.fmt = fmt_file(response_function)
            f.write(self.fmt)
            # then name the output file
            self.outp = output_fname
            f.write(self.outp)
            # then create a guess spectrum in flu format
            self.flu_file(guess_spectrum)
            f.write(self.flu_file)
            # then define the highest energy in the file
            self.maxE = maxE
            f.write("%15.10e" % maxE)
            # then request a chi2
            self.chi2 = chi2
            f.write("%15.10e" % maxE)
            # then request a temperature and reduction factor
            self.T = T
            self.eta = eta
            f.write("%15.10e, %15.10e" % (self.T, self.eta))
            # Then define the number of energy bins
            f.write("2, 2")
            # Then define the scale of the guess spectrum
            f.write("1")
            # Then define whether to use the maxed ds scale factor
            f.write("0")

    def run(self):
        subprocess.call(cmd)

    def read(self):
        something = True


class ibu_file(object):
    def __init__(self, fname, bs_sizes, bs_crs):
        edat = np.zeros((len(bs_sizes), 6))
        edat[:, 0] = bs_sizes[:]
        edat[:, 1] = bs_crs[:]
        edat[:, 2] = bs_u_crs[:]
        edat[:, 3] = 100.0 * bs_u_crs[:] / bs_crs[:] # change this to the percentage uncertainty
        edat[:, 4] = 0.0
        edat[:, 5] = range(len(bs_sizes))

        with open(fname + '.ibu', 'w') as fid:
            fid.write('0  *        d        cts / s\n')
            fid.write("%6s "% edat.shape[0] + '    0     Experimental/Predicted Cnts for \n')# + caseNames[caseInd]+"\n")
            for i in range(edat.shape[0]):
                fid.write('{0:<{1}}{2:<{3}}{4:<{5}}{6:<{7}}{8:<{9}}{10:<{11}}{12:<{13}}\n'.format(
                    str(edat[i,0]).replace(".","W"), 8,
                        "%.1f" % edat[i,0], 6,
                        "%.5e" % edat[i,1], 15,
                        "%.5e" % (edat[i,2]), 15,
                        "%.2f" % (edat[i,3]), 8,
                        "%.2e" % (edat[i,4]), 8,
                        str(int(edat[i,5])), 6))

class flu_file(object):
    def __init__(self, fname, Spc):
        with open(fname + '.flu', 'w') as fid:
            fid.write(" File eduGS_3.flu (norm.  exa.3: AHB50E.S11) / 25.11.2001\n")
            fid.write("           1          1                      fluence  given in 1/cm^2/MeV\n")
            fid.write("           2         %d          %d   %.3f\n" % (Spc.shape[0],Spc.shape[0], max(Spc[:,0])))
            for i in range(Spc.shape[0]):
                fid.write("    %1.5e  %1.5e  %1.5e\n" % (Spc[i,0],Spc[i,1],Spc[i,2]))

class fmt_file(object):
    def __init__(self, fname):
        dat=np.loadtxt('rms/mares1994.txt', skiprows=3)
        energs=dat[:,0]
        ball=dat[:,1:]
        # calibs=[0.85, 0.767, 0.651, 0.61, 0.61, 0.610, 0.61]
        calibs = [0.72, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72]
        for i in range(ball.shape[1]):
        	ball[:,i]=ball[:,i]*calibs[i]

        ball_desc=['0.0', '2.0', '3.0', '5.0', '8.0', '10.0', '12.0']
        with open(fname + '.fmt', 'w') as fid:
            fid.write('       MARCH-01-2004    *** ATTENTION: This file was specially compiled for UMG33\n')
            fid.write('Neutron Response Functions for BS with  5 enrg/decade, units: cm^2, pSv, pSv cm^2\n')
            fid.write('        %d   1\n' % len(energs))
            s1="\n%s       B_A*H Wgl  0d200    R-M by WIEGEL: NEMUS005.DAT, 14.12.2000\n"
            s2=" 1.000E+00      cm^2         0         0    3    1    1    0\n"
            kk=0
            for i in range(len(energs)):
            	if kk > 7:
            		fid.write("\n")
            		kk=0
            	kk=kk+1
            	fid.write(" %1.5e" % energs[i])
            fid.write("\n         0\n")
            fid.write('         %d' % (len(ball[0,:])))

            for i in range(len(ball[0,:])):
            	fid.write(s1 % ball_desc[i].replace(".","W"))
            	fid.write(s2)
            	kk=0
            	for j in range(len(ball[:,i])):
            		if kk > 7:
            			fid.write("\n")
            			kk=0
            		kk=kk+1
            		fid.write(" %9.3e" % ball[j,i])
