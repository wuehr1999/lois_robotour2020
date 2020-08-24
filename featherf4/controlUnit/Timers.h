#ifndef TIMERS_H
#define TIMERS_H

#include <Arduino.h>

/***
 * Inits 1 kHz timer.
 */
void start1000Hz();

/***
 * Interrupt Handler for 1 kHz timer
 */
void interrupt1000Hz();

/***
 * Inits 1 kHz timer.
 */
void start16000Hz();

/***
 * Interrupt Handler for 1 kHz timer
 */
void interrupt16000Hz();

#endif
