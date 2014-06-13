class FlyingText {
  
  String msg;
  float emphasis;
  double elapsed_time;
  float duration;
  float zoom_start, zoom_end;
  boolean started;
  
  float ox, oy;
  float rz;
  
  FlyingText()
  {
    started = false;
  }
  
  void go(String msg, float duration, float zoom_start, float zoom_end, float emphasis)
  {
    this.msg = msg;
    this.duration = duration;
    this.zoom_start = zoom_start;
    this.zoom_end = zoom_end;
    this.emphasis = emphasis;
    
    elapsed_time = 0.0;
    ox = oy = 0.0;
    rz = 0.0;
    
    started = true;
  }
  
  void updateAndDraw(double dt)
  {
    if(!started) return;
    if (elapsed_time > duration) 
    {
      started = false;
      return;
    }
    
    float k = (float)(elapsed_time / duration);
    float zoom = map(k*k, 0,1, zoom_start, zoom_end);
    zoom *= 2.0;
    float alpha = 2.5 - k*2.6;
    alpha = alpha > 1.0 ? 1.0 : alpha < 0.0 ? 0.0 : alpha;
    
    float ke = emphasis;
    ke *= ke;
    ox += random(-10, 10) * ke;
    oy += random(-10, 10) * ke;
    rz += random(-1, 1) * ke * PI / 60.0;
    
    float r = 1.0;
    float g = 1.0-ke*ke;
    float b = 1.0-ke*ke;
    
    fill(r*255.0, g*255.0, b*255.0,  alpha*255.0);
    
    pushMatrix();
    translate(width*0.5, height*0.5);
    scale(zoom, zoom);
    rotate(rz);
    text(msg, 0 + ox, 16 + oy);
    popMatrix();
    
    elapsed_time += dt;
  }

}

