Training: The Adventures of Sherlock Holmes
Testing: The Casebook of Sherlock Holmes

Q1: Which model performed worst and why might you have
    expected that model to have performed worst?

Answer: Bigram model (unsmoothed).  The bigram model (unsmoothed) failed to see most of          	the training bigrams in the testing data.  So it resulted in probabilities being
        0.

Q2: Did smoothing help or hurt the model’s ‘performance’
    when evaluated on this corpus? Why might that be?

Answer: Helped according to perplexity.  This could be a sparse data problem of course.  
        The smoothing was able to help in situations where it did indeed see the word(i) 
        in the dictionary but still was unable to see the previous word.  So we were left
        with just the equation (smoothing factor / v) since the probabilities were 0.  
        