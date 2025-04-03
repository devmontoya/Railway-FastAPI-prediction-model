from pydantic import BaseModel, Field

# This class indicates the features of the entered data
class Mobile(BaseModel):
    battery_power: int = Field(..., example=642)
    blue: int = Field(..., example=1)
    clock_speed: float = Field(..., example=0.5)
    dual_sim: int = Field(..., example=0)
    fc: int = Field(..., example=0)
    four_g: int = Field(..., example=1)
    int_memory: int = Field(..., example=38)
    m_dep: float = Field(..., example=0.8)
    mobile_wt: int = Field(..., example=86)
    n_cores: int = Field(..., example=5)
    pc: int = Field(..., example=10)
    px_height: int = Field(..., example=887)
    px_width: int = Field(..., example=1775)
    ram: int = Field(..., example=435)
    sc_h: int = Field(..., example=9)
    sc_w: int = Field(..., example=2)
    talk_time: int = Field(..., example=2)
    three_g: int = Field(..., example=1)
    touch_screen: int = Field(..., example=1)
    wifi: int = Field(..., example=0)

class Mobile_pd(BaseModel):
    id: int
    battery_power: int
    blue: int
    clock_speed: float
    dual_sim: int
    fc: int
    four_g: int
    int_memory: int
    m_dep: float
    mobile_wt: int
    n_cores: int
    pc: int
    px_height: int
    px_width: int
    ram: int
    sc_h: int
    sc_w: int
    talk_time: int
    three_g: int
    touch_screen: int
    wifi: int
    price_range_prediction: str