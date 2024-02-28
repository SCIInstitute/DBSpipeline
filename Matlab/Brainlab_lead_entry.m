targ = [8.07 9.45 1.89];
    acpc = 26.51;
    ctr = 17.37;
    t2 = 72.04;
    Proximal = [targ(1)+t2*sind(ctr), targ(2)+t2*sind(acpc)*sind(ctr), targ(3)+t2*cosd(acpc)*cosd(ctr)];
    