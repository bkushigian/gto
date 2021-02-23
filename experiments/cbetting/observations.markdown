# Observations about CBetting

## Flush Draws
There are some interesting patterns I'm noticing WRT betting on rainbow boards.
For instance, the following scenario:

LJ opens 2.5bb, BB calls

Pot: 5.5BB

Flop: 6d6c5s

BB checks

Looking at how LJ bets KQs, GTO+ gives the following table

| Hand | Equity | Bet 0.67 Pot Freq | Bet 0.33 Pot Freq | Check Freq |
|------|--------|-------------------|-------------------|------------|
| KcQc | 49.106 | 0                 | 0.328             | 0.672      |
| KdQd | 49.106 | 0                 | 0.328             | 0.672      |
| KsQs | 48.974 | 0.077             | 0.489             | 0.434      |
| KhQh | 46.007 | 0.168             | 0.458             | 0.374      |

KhQh has no flush BDFDs, but it bets 0.67 Pot more than any other KQs combo.
Why? Well, it seems to unblock a bunch of BDFDs, and we want to make life
difficult for them. By betting big without blocking any K or Q w/ a potential
BDFD we make it more likely that we are putting something like KsJs in a tough
position, having to pay more to see a turn card.

Another interesting thing: why is KsQs betting .67pot more than the other two
BDFD candidates? Here is my thought. What hands do we expect BB to call with?
Probably a lot of 5x, as well as a fair amount of 6x, OESDs, etc. This larger
bet targets the 5x holdings. Why? First, if they have 5x suited we know they
don't hold any spades, so they aren't blocking our flush draw. It's also good to
keep bottom pair in their range to try to get folds later (or now!)

**Question:** does this generalize? I'm going to look at a few more BDFD's in
LJ's cbetting range and see if there is a similar pattern.

KJs:

This doesn't even remotely hold for KJs.

This seems to hold for KTs, AKs, AQs. 

KTs:
+ KhTh: (Bet .67, Bet .33, Check) at (.128, .517, .355) 
+ KsTs: (Bet .67, Bet .33, Check) at (.123, .463, .415) 
+ KdTd: (Bet .67, Bet .33, Check) at (.077, .475, .448) 
+ KcTc: (Bet .67, Bet .33, Check) at (.077, .475, .448) 

AKs:

+ AhKh: (Bet .67, Bet .33, Check) at (.135, .484, .381) 
+ AsKs: (Bet .67, Bet .33, Check) at (.135, .484, .381) 
+ AdKd: (Bet .67, Bet .33, Check) at (.158, .514, .328) 
+ AcKc: (Bet .67, Bet .33, Check) at (.267, .499, .234) 

AQs:

+ AhQh: (Bet .67, Bet .33, Check) at (.068, .422, .571) 
+ AsQs: (Bet .67, Bet .33, Check) at (.068, .422, .571) 
+ AdQd: (Bet .67, Bet .33, Check) at (.030, .517, .453) 
+ AcQc: (Bet .67, Bet .33, Check) at (.157, .517, .326) 


