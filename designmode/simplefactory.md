# Simple Fctory Pattern

## Bibliography
大话设计模式	程杰	下的盗版

## Note
General concept of decoupling, narrowly decoupling of UI logic and service logic.

target: In aggregation relation, we use abstract and inherit to make put implementation off to class. Polymorphism is better than judgement conditions. This makes client know sless about implementation(less modification) and makes program open to extension and close to modification more(Only need to add more classes).

One specific implementation of open and close principle.

If one class has mutiple responsibilities, we should package functions into classes(or interfaces). And use abstract to further prevent modification.


## Example
Calculator, Aggregation calculation logic in one factory but not client.