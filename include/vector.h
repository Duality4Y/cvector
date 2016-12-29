#ifndef __VECTOR_H__
#define __VECTOR_H__

#include <math.h>
#include <stdio.h>

/* vector component type. */
typedef long double vectorcp_t;
/* vector struct containing vector components. */
typedef struct
{
    vectorcp_t x;
    vectorcp_t y;
    vectorcp_t z;
} vector_t;

/*
    vector operations. always returns a new vector.
    vector on vector has v prefix
    scalar on vector has s prefix
*/
vector_t vadd(vector_t, vector_t);
vector_t sadd(vector_t, vectorcp_t);

vector_t vsub(vector_t, vector_t);
vector_t ssub(vector_t, vectorcp_t);

vector_t vmul(vector_t, vector_t);
vector_t smul(vector_t, vectorcp_t);

/*
    small note, if 0 / 0 then it return leftside for that value.
    where the right hand side is zero.
*/
vector_t vdiv(vector_t, vector_t);
vector_t sdiv(vector_t, vectorcp_t);

/* magnitude operations. */
vectorcp_t get_magnitude(vector_t);
vector_t set_magnitude(vector_t, vectorcp_t);

vector_t normalize(vector_t);
vectorcp_t distance(vector_t, vector_t);
vectorcp_t dot(vector_t, vector_t);

#endif