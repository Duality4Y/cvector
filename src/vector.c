#include "vector.h"

vector_t vadd(vector_t lv, vector_t rv)
{
    vector_t result;
    
    result.x = lv.x + rv.x;
    result.y = lv.y + rv.y;
    result.z = lv.z + rv.z;

    return result;
}

vector_t sadd(vector_t lv, vectorcp_t rv)
{
    vector_t result;
    
    result.x = lv.x + rv;
    result.y = lv.y + rv;
    result.z = lv.z + rv;

    return result;
}

vector_t vsub(vector_t lv, vector_t rv)
{
    vector_t result;

    result.x = lv.x - rv.x;
    result.y = lv.y - rv.y;
    result.z = lv.z - rv.z;

    return result;
}

vector_t ssub(vector_t lv, vectorcp_t rv)
{
    vector_t result;

    result.x = lv.x - rv;
    result.y = lv.y - rv;
    result.z = lv.z - rv;

    return result;
}

vector_t vmul(vector_t lv, vector_t rv)
{
    vector_t result;

    result.x = lv.x * rv.x;
    result.y = lv.y * rv.y;
    result.z = lv.z * rv.z;

    return result;
}

vector_t smul(vector_t lv, vectorcp_t rv)
{
    vector_t result;

    result.x = lv.x * rv;
    result.y = lv.y * rv;
    result.z = lv.z * rv;

    return result;
}

vector_t vdiv(vector_t lv, vector_t rv)
{
    vector_t result;

    if(rv.x == 0) rv.x = 1;
    if(rv.y == 0) rv.y = 1;
    if(rv.z == 0) rv.z = 1;

    result.x = lv.x / rv.x;
    result.y = lv.y / rv.y;
    result.z = lv.z / rv.z;

    return result;
}

vector_t sdiv(vector_t lv, vectorcp_t rv)
{
    vector_t result;

    if(rv == 0) rv = 1;

    result.x = lv.x / rv;
    result.y = lv.y / rv;
    result.z = lv.z / rv;

    return result;
}

vectorcp_t get_magnitude(vector_t mag)
{
    vectorcp_t res = sqrt(mag.x * mag.x + mag.y * mag.y + mag.z * mag.z);
    
    return res;
}

vector_t set_magnitude(vector_t v, vectorcp_t val)
{
    vector_t nv;
    
    nv = normalize(v);
    nv = smul(nv, val);

    return nv;
}

vector_t normalize(vector_t v)
{
    vector_t nv;
    vectorcp_t mag;
    
    mag = get_magnitude(v);
    nv = sdiv(v, mag);
    
    return nv;
}

vectorcp_t distance(vector_t v1, vector_t v2)
{
    vector_t nv;

    nv = vsub(v1, v2);
    return get_magnitude(nv);
}

vectorcp_t dot(vector_t v1, vector_t v2)
{
    return ((v1.x * v2.x) + (v1.y * v2.y) + (v1.z * v2.z));
}