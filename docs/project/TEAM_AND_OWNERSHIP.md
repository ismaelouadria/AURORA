# Team and Ownership

## Purpose

AURORA uses ownership to create accountability, not silos.

A primary owner is responsible for driving a work area forward, maintaining its
documentation and evidence, and making its state understandable to the rest of the
team. Ownership does not prohibit another member from contributing.

A backup/reviewer exists to reduce single-person knowledge and provide meaningful
review. A backup is not required to duplicate the primary owner's implementation
knowledge immediately, but must be capable of understanding the subsystem,
interfaces, assumptions, current state, and recovery path.

## Team

| Member | Current primary technical area | Status |
|---|---|---|
| Ismael Ouadria | Safety controller, CRM/model-mismatch work, domain/data/validation coordination | Active |
| Abdulaziz | OPM Flow, EGG, higher-fidelity reservoir simulation | Active |
| Abdurrahman | AI controller, RL environment, PPO/recurrent controller | Active |
| Mahdi Bouakline | Data, telemetry, provenance, experiment infrastructure | Active |
| Timur | Scope pending team/supervisor decision | Unresolved |

Timur's final specialization, including the possible role of hardware, is deliberately
not decided here. No core dependency should assume the outcome until the decision is
made and recorded.

## GitHub primary-owner routing

GitHub issue assignment uses the following canonical routing for unambiguous
technical workstreams:

| Routing label | Primary owner | GitHub |
|---|---|---|
| `safety-controller` | Ismael Ouadria | `@ismaelouadria` |
| `simulation` | Abdulaziz | `@abdulaziz-alsibakhi` |
| `ai-controller` | Abdurrahman | `@AbduCh04` |
| `data-logging` | Mahdi Bouakline | `@BouaklineMahdi` |

This routing establishes the default **primary** assignee. It does not establish
exclusive ownership and it does not automatically choose the backup/reviewer.

Cross-cutting labels such as `system-design`, `integration`, `validation`,
`documentation`, `experiments`, `decision`, and `demo` are deliberately not
auto-routed because their primary owner depends on the specific outcome.

If an issue contains more than one of the four routing labels above and they map
to different people, automation must not guess the primary owner. The issue
requires explicit ownership resolution.

Timur is deliberately excluded from automatic routing until his specialization
is resolved through the corresponding project decision.

## Primary owner responsibilities

A primary owner should:

- understand the purpose and requirements of the owned area;
- keep its canonical documentation current;
- identify unresolved assumptions rather than silently choosing them;
- implement or coordinate the required work;
- provide tests and evidence appropriate to the work;
- communicate interface changes to dependent owners;
- make progress visible through GitHub;
- leave enough durable context that another teammate can continue the work.

## Backup/reviewer responsibilities

A backup/reviewer should:

- understand the subsystem's role in the full AURORA loop;
- understand its inputs, outputs, major assumptions, and failure modes;
- review consequential changes;
- know where setup instructions, evidence, and current issues live;
- be able to continue or coordinate recovery if the primary owner is unavailable.

## Backup assignments

Specific backup assignments are not yet frozen.

They must be agreed by the team rather than inferred from historical planning material.
Phase 0 is not complete until important workstreams have an explicit primary and
backup/reviewer.

## Shared-understanding rule

Every member should be able to explain:

1. the complete AURORA control loop;
2. the project's central model-mismatch problem;
3. their own subsystem in meaningful technical depth;
4. the interfaces immediately upstream and downstream of their subsystem;
5. the important assumptions and limitations affecting their work; and
6. how their work contributes evidence to the project.

The project must not depend on a single member being the only person capable of
explaining an important subsystem.

## Ownership changes

Ownership may change.

A consequential ownership change should update this document and affected GitHub
issues. If the change also alters architecture or project scope, follow the change
control process.
