// variant defining pseudo multi-entrypoint actions
type ledger is map(address, bool);
type storage is record
	balanceofvotes: ledger;
	owner: address;
	contractPause: bool;
	yesVotes: int;
	noVotes: int;
end

type action is
| SetAdmin of address
| Pause of bool
| Yes of bool
| No of bool
| Reset of unit


function isAdmin (const s : storage) : bool is
  block {skip} with (sender = s.owner)

function isPause (const s : storage) : bool is
  block{skip} with (s.contractPause)

function setPause (const s : storage; const setter : bool) : storage is
  block{s.contractPause := setter} with s

function setAdmin(const s : storage ; const addr : address) : storage is
  block {
  	  if(isAdmin(s)) then s.owner := addr;
      else failwith("Admin not set");
   } with s


function votingYes(const vote : bool; const s : storage) : (storage) is
  block {
      if ( isPause(s) = False ) then block {
        if ( isAdmin(s) = False )
          then block {
           case s.balanceofvotes[sender] of
             | Some (bool) -> failwith("You have already voted !")
             | None -> block {
               s.balanceofvotes[sender] := vote;
               s.yesVotes := s.yesVotes + 1;
               if (s.yesVotes + s.noVotes = 10) then block {
                 s.contractPause := True;
               }
              else block {
                  skip
                }
            }
          end
        }
      else block {
        failwith("The administrator can't vote");
       }
     }
     else block {
       failwith("The contract is paused");
    }
  } with (s)

function votingNo(const vote : bool; const s : storage) : (storage) is
  block {
      if (isPause(s) = False) then block {
        if ( isAdmin(s) = False )
          then block {
           case s.balanceofvotes[sender] of
             | Some (bool) -> failwith("You have already voted !")
             | None -> block {
               s.balanceofvotes[sender] := vote;
               s.noVotes := s.noVotes + 1;
               if (s.yesVotes + s.noVotes = 10) then block {
                 s.contractPause := True;
               }
              else block {
                  skip
                }
            }
          end
        }
      else block {
        failwith("The administrator can't vote");
       }
     }
     else block {
       failwith("The contract is paused");
    }
  } with (s)

function submitReset (const s : storage) : (storage) is
  block {
    if ( isAdmin(s) )
      then block {
        if ( isPause(s) )
          then block {
            for i in map s.balanceofvotes block {
              remove i from map s.balanceofvotes;
            };
            s.contractPause := False;
          }
          else block {
            failwith("The contract is paused");
          }
      }
      else block {
        failwith("You need to be administrator to run the function");
      }
  } with (s)


// real entrypoint that re-routes the flow based
// on the action provided
function main (const p : action ; const s : storage) :
  (list(operation) * storage) is
  block { skip } with ((nil : list(operation)),
  case p of
  | Pause(b) -> setPause(s, b)
  | SetAdmin(a) -> setAdmin(s, a)
  | Yes(c) -> votingYes(c, s)
  | No(d) -> votingNo(d, s)
  | Reset -> submitReset(s)
end)