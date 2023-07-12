# Software Design by Example

Most data scientists have taught themselves most of what they know
about programming.  As a result, many have gaps in their knowledge:
they may be experts in some areas, but don't even know what they don't
know about others.

One of those other areas is software design.  A large program is not
just a dozen short programs stacked on top of each other: doubling the
size of a program more than doubles its complexity.  Since our brains
can only hold a small number of things at once, making large programs
comprehensible, testable, shareable, and maintainable requires more
than using functions and sensible variable names: it requires design.

The best way to learn design in any field is to study examples.  These
lessons therefore build small versions of tools that programmers use
every day to show how experienced software designers think.  Along the
way, they introduce some fundamental ideas in computer science that
most data scientists haven't encountered.  Finally, we hope that if
you know how programming tools work, you'll be more likely to use them
and better able to use them well.

<table>
    <thead>
        <tr>
            <th>Title</th>
            <th>Slides</th>
            <th>Words</th>
            <th>Sections</th>
            <th>Exercises</th>
            <th>Figures</th>
            <th>Syllabus</th>
            <th>Index</th>
            <th>Glossary</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>intro</td>
            <td><span style=&quot;color:green&quot;>11</span></td>
            <td><span style=&quot;color:green&quot;>1324</span></td>
            <td><span style=&quot;color:green&quot;>7</span></td>
            <td><span style=&quot;color:green&quot;>2</span></td>
            <td><span style=&quot;color:green&quot;>2</span></td>
            <td><span style=&quot;color:green&quot;>4</span></td>
            <td><span style=&quot;color:green&quot;>3</span></td>
            <td><span style=&quot;color:green&quot;>0</span></td>
        </tr>
        <tr>
            <td>oop</td>
            <td><span style=&quot;color:green&quot;>18</span></td>
            <td><span style=&quot;color:red&quot;>1200</span></td>
            <td><span style=&quot;color:green&quot;>5</span></td>
            <td><span style=&quot;color:green&quot;>4</span></td>
            <td><span style=&quot;color:green&quot;>4</span></td>
            <td><span style=&quot;color:green&quot;>6</span></td>
            <td><span style=&quot;color:green&quot;>11</span></td>
            <td><span style=&quot;color:green&quot;>9</span></td>
        </tr>
        <tr>
            <td>dup</td>
            <td><span style=&quot;color:green&quot;>20</span></td>
            <td><span style=&quot;color:green&quot;>1820</span></td>
            <td><span style=&quot;color:green&quot;>5</span></td>
            <td><span style=&quot;color:green&quot;>5</span></td>
            <td><span style=&quot;color:green&quot;>5</span></td>
            <td><span style=&quot;color:green&quot;>5</span></td>
            <td><span style=&quot;color:green&quot;>2</span></td>
            <td><span style=&quot;color:green&quot;>10</span></td>
        </tr>
        <tr>
            <td>glob</td>
            <td><span style=&quot;color:green&quot;>23</span></td>
            <td><span style=&quot;color:green&quot;>1813</span></td>
            <td><span style=&quot;color:green&quot;>4</span></td>
            <td><span style=&quot;color:green&quot;>8</span></td>
            <td><span style=&quot;color:green&quot;>4</span></td>
            <td><span style=&quot;color:green&quot;>6</span></td>
            <td><span style=&quot;color:green&quot;>1</span></td>
            <td><span style=&quot;color:green&quot;>14</span></td>
        </tr>
        <tr>
            <td>parse</td>
            <td><span style=&quot;color:green&quot;>16</span></td>
            <td><span style=&quot;color:green&quot;>1352</span></td>
            <td><span style=&quot;color:green&quot;>4</span></td>
            <td><span style=&quot;color:green&quot;>5</span></td>
            <td><span style=&quot;color:green&quot;>3</span></td>
            <td><span style=&quot;color:green&quot;>7</span></td>
            <td><span style=&quot;color:green&quot;>5</span></td>
            <td><span style=&quot;color:green&quot;>12</span></td>
        </tr>
        <tr>
            <td>test</td>
            <td><span style=&quot;color:green&quot;>17</span></td>
            <td><span style=&quot;color:green&quot;>1958</span></td>
            <td><span style=&quot;color:green&quot;>5</span></td>
            <td><span style=&quot;color:green&quot;>7</span></td>
            <td><span style=&quot;color:green&quot;>4</span></td>
            <td><span style=&quot;color:green&quot;>4</span></td>
            <td><span style=&quot;color:green&quot;>9</span></td>
            <td><span style=&quot;color:green&quot;>14</span></td>
        </tr>
        <tr>
            <td>interp</td>
            <td><span style=&quot;color:green&quot;>17</span></td>
            <td><span style=&quot;color:green&quot;>2036</span></td>
            <td><span style=&quot;color:green&quot;>5</span></td>
            <td><span style=&quot;color:green&quot;>8</span></td>
            <td><span style=&quot;color:green&quot;>3</span></td>
            <td><span style=&quot;color:green&quot;>6</span></td>
            <td><span style=&quot;color:green&quot;>10</span></td>
            <td><span style=&quot;color:green&quot;>15</span></td>
        </tr>
        <tr>
            <td>func</td>
            <td><span style=&quot;color:green&quot;>20</span></td>
            <td><span style=&quot;color:green&quot;>1433</span></td>
            <td><span style=&quot;color:green&quot;>5</span></td>
            <td><span style=&quot;color:green&quot;>4</span></td>
            <td><span style=&quot;color:green&quot;>3</span></td>
            <td><span style=&quot;color:green&quot;>7</span></td>
            <td><span style=&quot;color:green&quot;>6</span></td>
            <td><span style=&quot;color:green&quot;>13</span></td>
        </tr>
        <tr>
            <td>reflect</td>
            <td><span style=&quot;color:green&quot;>20</span></td>
            <td><span style=&quot;color:green&quot;>1971</span></td>
            <td><span style=&quot;color:green&quot;>6</span></td>
            <td><span style=&quot;color:green&quot;>4</span></td>
            <td><span style=&quot;color:green&quot;>3</span></td>
            <td><span style=&quot;color:green&quot;>7</span></td>
            <td><span style=&quot;color:green&quot;>10</span></td>
            <td><span style=&quot;color:green&quot;>7</span></td>
        </tr>
        <tr>
            <td>archive</td>
            <td><span style=&quot;color:green&quot;>20</span></td>
            <td><span style=&quot;color:green&quot;>2182</span></td>
            <td><span style=&quot;color:green&quot;>6</span></td>
            <td><span style=&quot;color:green&quot;>7</span></td>
            <td><span style=&quot;color:green&quot;>3</span></td>
            <td><span style=&quot;color:green&quot;>5</span></td>
            <td><span style=&quot;color:green&quot;>14</span></td>
            <td><span style=&quot;color:green&quot;>14</span></td>
        </tr>
        <tr>
            <td>check</td>
            <td><span style=&quot;color:green&quot;>21</span></td>
            <td><span style=&quot;color:green&quot;>1545</span></td>
            <td><span style=&quot;color:green&quot;>5</span></td>
            <td><span style=&quot;color:green&quot;>6</span></td>
            <td><span style=&quot;color:green&quot;>3</span></td>
            <td><span style=&quot;color:green&quot;>5</span></td>
            <td><span style=&quot;color:green&quot;>12</span></td>
            <td><span style=&quot;color:green&quot;>13</span></td>
        </tr>
        <tr>
            <td>template</td>
            <td><span style=&quot;color:green&quot;>24</span></td>
            <td><span style=&quot;color:green&quot;>2260</span></td>
            <td><span style=&quot;color:green&quot;>7</span></td>
            <td><span style=&quot;color:green&quot;>10</span></td>
            <td><span style=&quot;color:green&quot;>3</span></td>
            <td><span style=&quot;color:green&quot;>4</span></td>
            <td><span style=&quot;color:green&quot;>20</span></td>
            <td><span style=&quot;color:green&quot;>6</span></td>
        </tr>
        <tr>
            <td>lint</td>
            <td><span style=&quot;color:green&quot;>21</span></td>
            <td><span style=&quot;color:green&quot;>2234</span></td>
            <td><span style=&quot;color:green&quot;>6</span></td>
            <td><span style=&quot;color:green&quot;>7</span></td>
            <td><span style=&quot;color:green&quot;>3</span></td>
            <td><span style=&quot;color:green&quot;>4</span></td>
            <td><span style=&quot;color:green&quot;>16</span></td>
            <td><span style=&quot;color:green&quot;>3</span></td>
        </tr>
        <tr>
            <td>layout</td>
            <td><span style=&quot;color:green&quot;>18</span></td>
            <td><span style=&quot;color:green&quot;>2295</span></td>
            <td><span style=&quot;color:green&quot;>6</span></td>
            <td><span style=&quot;color:green&quot;>10</span></td>
            <td><span style=&quot;color:green&quot;>7</span></td>
            <td><span style=&quot;color:green&quot;>5</span></td>
            <td><span style=&quot;color:green&quot;>15</span></td>
            <td><span style=&quot;color:green&quot;>9</span></td>
        </tr>
        <tr>
            <td>perf</td>
            <td><span style=&quot;color:green&quot;>23</span></td>
            <td><span style=&quot;color:blue&quot;>3265</span></td>
            <td><span style=&quot;color:green&quot;>6</span></td>
            <td><span style=&quot;color:green&quot;>11</span></td>
            <td><span style=&quot;color:green&quot;>8</span></td>
            <td><span style=&quot;color:green&quot;>4</span></td>
            <td><span style=&quot;color:green&quot;>17</span></td>
            <td><span style=&quot;color:green&quot;>14</span></td>
        </tr>
        <tr>
            <td>persist</td>
            <td><span style=&quot;color:green&quot;>16</span></td>
            <td><span style=&quot;color:blue&quot;>3252</span></td>
            <td><span style=&quot;color:green&quot;>6</span></td>
            <td><span style=&quot;color:green&quot;>10</span></td>
            <td><span style=&quot;color:green&quot;>4</span></td>
            <td><span style=&quot;color:green&quot;>5</span></td>
            <td><span style=&quot;color:green&quot;>14</span></td>
            <td><span style=&quot;color:green&quot;>7</span></td>
        </tr>
        <tr>
            <td>binary</td>
            <td><span style=&quot;color:green&quot;>26</span></td>
            <td><span style=&quot;color:blue&quot;>3900</span></td>
            <td><span style=&quot;color:green&quot;>6</span></td>
            <td><span style=&quot;color:green&quot;>6</span></td>
            <td><span style=&quot;color:green&quot;>4</span></td>
            <td><span style=&quot;color:green&quot;>5</span></td>
            <td><span style=&quot;color:green&quot;>6</span></td>
            <td><span style=&quot;color:green&quot;>20</span></td>
        </tr>
        <tr>
            <td>db</td>
            <td><span style=&quot;color:green&quot;>26</span></td>
            <td><span style=&quot;color:green&quot;>2254</span></td>
            <td><span style=&quot;color:green&quot;>8</span></td>
            <td><span style=&quot;color:green&quot;>4</span></td>
            <td><span style=&quot;color:green&quot;>4</span></td>
            <td><span style=&quot;color:green&quot;>5</span></td>
            <td><span style=&quot;color:green&quot;>11</span></td>
            <td><span style=&quot;color:green&quot;>7</span></td>
        </tr>
        <tr>
            <td>build</td>
            <td><span style=&quot;color:green&quot;>19</span></td>
            <td><span style=&quot;color:green&quot;>1836</span></td>
            <td><span style=&quot;color:green&quot;>5</span></td>
            <td><span style=&quot;color:green&quot;>8</span></td>
            <td><span style=&quot;color:green&quot;>4</span></td>
            <td><span style=&quot;color:green&quot;>5</span></td>
            <td><span style=&quot;color:green&quot;>12</span></td>
            <td><span style=&quot;color:green&quot;>17</span></td>
        </tr>
        <tr>
            <td>pack</td>
            <td><span style=&quot;color:green&quot;>24</span></td>
            <td><span style=&quot;color:blue&quot;>2926</span></td>
            <td><span style=&quot;color:green&quot;>7</span></td>
            <td><span style=&quot;color:green&quot;>8</span></td>
            <td><span style=&quot;color:green&quot;>4</span></td>
            <td><span style=&quot;color:green&quot;>7</span></td>
            <td><span style=&quot;color:green&quot;>11</span></td>
            <td><span style=&quot;color:green&quot;>11</span></td>
        </tr>
        <tr>
            <td>ftp</td>
            <td><span style=&quot;color:green&quot;>20</span></td>
            <td><span style=&quot;color:green&quot;>1821</span></td>
            <td><span style=&quot;color:green&quot;>5</span></td>
            <td><span style=&quot;color:green&quot;>4</span></td>
            <td><span style=&quot;color:green&quot;>3</span></td>
            <td><span style=&quot;color:green&quot;>4</span></td>
            <td><span style=&quot;color:green&quot;>6</span></td>
            <td><span style=&quot;color:green&quot;>10</span></td>
        </tr>
        <tr>
            <td>http</td>
            <td><span style=&quot;color:green&quot;>19</span></td>
            <td><span style=&quot;color:green&quot;>2273</span></td>
            <td><span style=&quot;color:green&quot;>5</span></td>
            <td><span style=&quot;color:green&quot;>9</span></td>
            <td><span style=&quot;color:green&quot;>3</span></td>
            <td><span style=&quot;color:green&quot;>5</span></td>
            <td><span style=&quot;color:green&quot;>14</span></td>
            <td><span style=&quot;color:green&quot;>12</span></td>
        </tr>
        <tr>
            <td>viewer</td>
            <td><span style=&quot;color:blue&quot;>33</span></td>
            <td><span style=&quot;color:blue&quot;>2982</span></td>
            <td><span style=&quot;color:green&quot;>7</span></td>
            <td><span style=&quot;color:green&quot;>4</span></td>
            <td><span style=&quot;color:red&quot;>2</span></td>
            <td><span style=&quot;color:green&quot;>7</span></td>
            <td><span style=&quot;color:green&quot;>9</span></td>
            <td><span style=&quot;color:green&quot;>8</span></td>
        </tr>
        <tr>
            <td>undo</td>
            <td><span style=&quot;color:green&quot;>21</span></td>
            <td><span style=&quot;color:green&quot;>1392</span></td>
            <td><span style=&quot;color:green&quot;>5</span></td>
            <td><span style=&quot;color:green&quot;>5</span></td>
            <td><span style=&quot;color:red&quot;>1</span></td>
            <td><span style=&quot;color:green&quot;>4</span></td>
            <td><span style=&quot;color:green&quot;>7</span></td>
            <td><span style=&quot;color:green&quot;>3</span></td>
        </tr>
        <tr>
            <td>vm</td>
            <td><span style=&quot;color:green&quot;>20</span></td>
            <td><span style=&quot;color:green&quot;>2249</span></td>
            <td><span style=&quot;color:green&quot;>6</span></td>
            <td><span style=&quot;color:green&quot;>10</span></td>
            <td><span style=&quot;color:green&quot;>6</span></td>
            <td><span style=&quot;color:green&quot;>4</span></td>
            <td><span style=&quot;color:green&quot;>7</span></td>
            <td><span style=&quot;color:green&quot;>13</span></td>
        </tr>
        <tr>
            <td>debugger</td>
            <td><span style=&quot;color:green&quot;>22</span></td>
            <td><span style=&quot;color:blue&quot;>2820</span></td>
            <td><span style=&quot;color:green&quot;>6</span></td>
            <td><span style=&quot;color:green&quot;>10</span></td>
            <td><span style=&quot;color:green&quot;>4</span></td>
            <td><span style=&quot;color:green&quot;>4</span></td>
            <td><span style=&quot;color:green&quot;>9</span></td>
            <td><span style=&quot;color:green&quot;>7</span></td>
        </tr>
        <tr>
            <td>finale</td>
            <td><span style=&quot;color:red&quot;>4</span></td>
            <td><span style=&quot;color:red&quot;>582</span></td>
            <td><span style=&quot;color:red&quot;>0</span></td>
            <td><span style=&quot;color:red&quot;>0</span></td>
            <td><span style=&quot;color:red&quot;>1</span></td>
            <td><span style=&quot;color:red&quot;>0</span></td>
            <td><span style=&quot;color:green&quot;>4</span></td>
            <td><span style=&quot;color:green&quot;>0</span></td>
        </tr>
        <tr>
            <td>---</td>
            <td>---</td>
            <td>---</td>
            <td>---</td>
            <td>---</td>
            <td>---</td>
            <td>---</td>
            <td>---</td>
            <td>---</td>
        </tr>
        <tr>
            <td>Target</td>
            <td>15-26</td>
            <td>1300-2300</td>
            <td>2-8</td>
            <td>4-14</td>
            <td>3-8</td>
            <td>4-8</td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>Average</td>
            <td>2110</td>
            <td>20.0</td>
            <td>5.5</td>
            <td>6.5</td>
            <td>3.6</td>
            <td>5.0</td>
            <td>9.7</td>
            <td>9.9</td>
        </tr>
        <tr>
            <td>Total</td>
            <td>539</td>
            <td>56975</td>
            <td>148</td>
            <td>176</td>
            <td>98</td>
            <td>134</td>
            <td>261</td>
            <td>268</td>
        </tr>
    </tbody>
</table>
