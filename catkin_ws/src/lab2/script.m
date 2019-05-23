

syms theta2
syms theta3
syms D1
syms A3
syms E;
syms r11;
syms r12;
syms r13;
syms r14;
syms r21;
syms r22;
syms r23;
syms r24;
syms r31;
syms r32;
syms r33;
syms r34;

M1 = [[1 0 0 0];[0 1 0 0];[ 0 0 1 D1];[0 0 0 1]];


M2 = [[cos(theta2) -sin(theta2) 0 0];[sin(theta2) cos(theta2) 0 0];[0 0 1 0]; [0 0 0 1]];

M3 = [[cos(theta3) -sin(theta3) 0 A3];[sin(theta3) cos(theta3) 0 0];[ 0 0 1 0];[0 0 0 1]];

M4 = [[1 0 0 E];[0 1 0 0];[ 0 0 1 0];[0 0 0 1]];

END = M1 * M2 * M3 * M4;

R = [[r11 r12 r13 r14];[r21 r22 r23 r24];[ r31 r32 r33 r34];[0 0 0 1]];


% Rafal's solution
%M1 =  [[1 0 0 0];[0 1 0 0];[ 0 0 1 r34];[0 0 0 1]];
%Y=R*M4^(-1);
%X=M1*M2*M3;
%eqn = X==Y;

eqn = END == R;
%equations = [eqn(1, 1), eqn(1, 2), eqn(2, 1), eqn(3, 1), eqn(2, 2), eqn(3, 3), eqn(2, 1), eqn(3, 2), eqn(3, 1), eqn(4, 1),eqn(4, 2), eqn(4, 3)];
equations = [eqn(1, 4), eqn(2, 4), eqn(3, 4)];
result = solve(equations, ...
                [theta2, theta3, D1]);
            
            
