SELECT 
lambdas + (1-lambdas) * (1/(1+exp(-1.702*disc*(0 - diff)))) as correct_rate, quiz.quiz ,diff
FROM public.quiz
where lambdas + (1-lambdas) * (1/(1+exp(-1.702*disc*(0 - diff)))) > 0.8
limit 100

