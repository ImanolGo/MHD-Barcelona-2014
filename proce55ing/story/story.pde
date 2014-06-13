import oscP5.*;
import netP5.*;
  
OscP5 oscP5;

PFont f;

FlyingText[] texts = new FlyingText[8];
int current_text = 0;
double time_seconds_old;  

boolean is_fullscreen = true;

void setup() 
{
  if(is_fullscreen)
  {
    size(displayWidth, displayHeight);
  }
  else
  {
    size(displayWidth/2, displayHeight/2);
  }
  frameRate(60);
  
  for(int i = 0; i < texts.length; i++)
  {
    texts[i] = new FlyingText();
  }
  //printArray(PFont.list());
  f = createFont("Georgia", 64);
  textFont(f);
  textAlign(CENTER);
  
  /* start oscP5, listening for incoming messages at port 12000 */
  oscP5 = new OscP5(this, 12000);
}

boolean sketchFullScreen() 
{
  return is_fullscreen;
}

void draw() 
{
  double time_seconds = millis() / 1000.0;
  double dt = time_seconds - time_seconds_old;  
  double seconds = millis() / 1000.0;
  
  background(0);
  
  for(FlyingText txt : texts)
  {
    txt.updateAndDraw(dt);
  }
  
  time_seconds_old = time_seconds;
}

/* incoming osc message are forwarded to the oscEvent method. */
void oscEvent(OscMessage msg) 
{
  /* print the address pattern and the typetag of the received OscMessage */
  println("### received an osc message.");
  println(" addrpattern: " + msg.addrPattern());
  println(" typetag: " + msg.typetag());
  if(msg.checkAddrPattern("/text") == true)
  if(msg.checkTypetag("si"))
  {
    String txt = msg.get(0).stringValue();
    float emphasis = msg.get(1).intValue() / 1000.0;
    
    float duration = 2.0 - emphasis;
    float zoom_start = 1.0;
    float zoom_end = 6.0 + 4.0*emphasis;
    
    texts[current_text].go(txt, duration, zoom_start, zoom_end, emphasis);
    current_text++;
    current_text %= texts.length;
  }
}


