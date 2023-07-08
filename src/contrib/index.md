Contributions are very welcome;
please contact us by email or by filing an issue on this site.
All contributors must abide by our Code of Conduct.

## FAQ {: #contrib-faq}

Why don't the examples connect with each other? For example, why don't they build toward a complete minimal IDE?

:   It was tempting, but my attempts to do this in the past have never gone well.
    First, it makes maintenance much more difficult
    because a change in an early chapter may have knock-on effects on several subsequent chapters.
    Second, it constraints what is taught and in what order:
    if the examples are independent of each other,
    instructors can pick and choose the pieces that are most relevant to their audience and goals.

Can I contribute a chapter?

:   Absolutely, and if enough people do that we will publish a second volume.
    Some things I'd particularly like to see are:

    -   An object-relational mapper to show people how tools like [SQLAlchemy][sqlalchemy] work
        ([% issue 45 %]).
    -   A discrete event simulator to show people how tools like [SimPy][simpy] work
        and to explore co-operative concurrency using generators
        ([% issue 56 %]).
    -   An issue-tracking system, mostly to show how workflow management and authentication work
        ([% issue 82 %]).
    -   Another build system that uses publish/subscribe instead of the top-down approach of [%x build %]
        ([% issue 83 %]).
    -   A fuzz tester that uses some of the ideas from [%b Zeller2023 %]
        ([% issue 84 %]).
    -   A package installer to complement the package manager of [%x pack %]
        ([% issue 121 %]).
    -   A file compression tool like `zip`
        ([% issue 144 %]).
    -   A database that uses B-trees instead of a log for storage
        ([% issue 151 %]).

## Making Decisions {: #contrib-decisions}

This project uses [Martha's Rules][marthas_rules] for consensus decision making:

1.  Before each meeting, anyone who wishes may sponsor a proposal by filing an
    issue in the GitHub repository tagged "proposal".  People must file proposals
    at least 24 hours before a meeting in order for them to be considered at that
    meeting, and must include:
    -   a one-line summary (the subject line of the issue)
    -   the full text of the proposal
    -   any required background information
    -   pros and cons
    -   possible alternatives

2.  A quorum is established in a meeting if half or more of voting members are
    present.

3.  Once a person has sponsored a proposal, they are responsible for it.  The
    group may not discuss or vote on the issue unless the sponsor or their
    delegate is present.  The sponsor is also responsible for presenting the
    item to the group.

4.  After the sponsor presents the proposal, a "sense" vote is cast for the
    proposal before any discussion:
    -   Who likes the proposal?
    -   Who can live with the proposal?
    -   Who is uncomfortable with the proposal?

5.  If everyone likes or can live with the proposal, it passes immediately.

6.  If most of the group is uncomfortable with the proposal, it is postponed for
    further rework by the sponsor.

7.  Otherwise, members who are uncomfortable can briefly state their objections.
    A timer is then set for a brief discussion moderated by the facilitator.
    After 10 minutes or when no one has anything further to add (whichever comes
    first), the facilitator calls for a yes-or-no vote on the question: "Should
    we implement this decision over the stated objections?"  If a majority votes
    "yes" the proposal is implemented.  Otherwise, the proposal is returned to
    the sponsor for further work.
